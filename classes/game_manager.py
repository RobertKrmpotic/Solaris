import yaml
import glob

from classes.player import Player
from classes.deck import Deck
from classes.card import Card

from classes.utils import create_deck_dict, create_deck_list
class GameManager:
    def __init__(self):
        self.player1= Player(1)
        self.player2= Player(2)
        self.turn_n = 0
        self.phase = "pre_start"
        self.limbo = []
        self.visible_cards = []
        self.planet_deck = []
        self.spell_deck = []
        self.trap_deck = []
        self.invaders_deck = []
        self.star_deck = []

        self.pre_start()
    
    def get_players(self):
        return [self.player1, self.player2]

    def switch_lists(self,card,from_list, to_list):
        ''' Takes a card from one list and append it to the other '''
        to_list.append(card)
        from_list.remove(card)

    def play_planet(self, player, planet):
        #check if allowed
        self.switch_lists(planet, player.hand, player.galaxy)


    def deal_cards(self,deck, n):
        for _ in range(0,n):
            self.player1.hand.append( deck.list.pop())
            self.player2.hand.append( deck.list.pop())

    def assign_stars(self):
        ''' assign a star to each player'''
        for player in self.get_players():
            player.star = self.star_deck.list.pop()
            player.move_star()
        print("assigning stars")

    def planet_deck_start(self):
        ''' Load planet cards and assign self.planet_deck and deal starting cards'''
        self.planet_deck_dict = create_deck_dict("Planet")
        planet_deck_list = create_deck_list(self.planet_deck_dict)
        self.planet_deck = Deck(planet_deck_list)
        self.planet_deck.shuffle_deck()
        self.deal_cards(self.planet_deck,2)
    
    def star_deck_start(self):
        ''' Load cards, create star deck and assign stars to players'''
        self.star_deck_dict = create_deck_dict("Star")
        print(self.star_deck_dict)
        star_deck_list = create_deck_list(self.star_deck_dict)
        self.star_deck = Deck(star_deck_list)
        self.star_deck.shuffle_deck()
        self.assign_stars()
        

    def pre_start(self):
        ''' do a setup for turn 0'''
        self.planet_deck_start()
        self.star_deck_start()
        
    
    def sort_hands(self):
        ''' Sorts correct position of sprites in hand'''
        for player in self.get_players():
            player.sort_hand()

    def next_phase(self):
        if self.phase == "pre_start":
            self.phase = "start"