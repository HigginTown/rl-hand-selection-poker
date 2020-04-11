import treys
import gym 
from gym import spaces
from itertools import compress
import numpy as np

class HandMaker(gym.Env):
    def __init__(self):
        self.evaluator = treys.evaluator.Evaluator()
        self.deck = treys.deck.Deck()
        self.card_ints = self.deck.draw(13)
        self.card_strings = [treys.Card.int_to_str(c) for c in self.card_ints]
        self.done = False
        self.reward_range = (0,1)
        self.action_space = gym.spaces.multi_binary.MultiBinary(13) # select from 13 cards
        self.observation_space = gym.spaces.multi_binary.MultiBinary(416) # 32 bits * 13 cards

    def _get_obs(self):
        # the observation is the encoded representation of the cards
        # get 13 cards and convert them to binary strings
     
        return np.array([item for sublist in [[int(i) for i in y] for y in [f'{a:032b}' for a in self.card_ints]] for item in sublist])
    
    def _get_reward(self, five_cards):
        """Return 1 minus the rank class percentage for the five card hand
        The worst hand has a value of 1, while a Royal Flush has a value of 0
        If we return 1 - this value, we return a reward in [0,1] where the 
        higher number is a better reward.
        """
        
        return 1-self.evaluator.get_five_card_rank_percentage(self.evaluator._five(five_cards))
    
    def step(self, action):
        # set the state of the game to done
        self.done = True 
        
        # if the action is invalid, get a negative reward and exit
        if sum(action) != 5: return (self._get_obs(), -1, self.done, {})
        
        # otherwise, we get the subset of cards based on the valid action
        # we need the 5 cards selected from the 13 for evaluation
        self.selected_cards = list(compress(self.card_ints, action))
        self.reward = self._get_reward(self.selected_cards)
        
        
        return (self._get_obs(), self.reward, self.done, {})
        
    def reset(self):
        self.deck = treys.deck.Deck()
        self.done = False
        self.card_ints = seld.deck.draw(13)
        return self._get_obs()
        