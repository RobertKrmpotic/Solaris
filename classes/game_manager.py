import yaml
import glob

from classes.player import Player
from classes.deck import Deck
from classes.card import Card
from classes.turn_manager import TurnManager

from classes.utils import create_deck_dict, create_deck_list
class GameManager:
    def __init__(self):
        self.player1= Player(1)
        self.player2= Player(2)
        self.players = {1:self.player1, 2:self.player2}
        self.turn_manager = TurnManager()
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
        player.sort_hand()
        player.sort_galaxy()
        player.player_created = True

    
    def deal_card(self,deck, owner):
        card = deck.list.pop()
        card.owner = owner
        self.players[owner].hand.append(card)
        self.visible_cards.append(card)


    def deal_cards(self,deck, n):
        print("dealing")
        for _ in range(0,n):
            self.deal_card(deck,1)
            self.deal_card(deck,2)

    def assign_stars(self):
        ''' assign a star to each player'''
        for player in self.get_players():
            player.star = self.star_deck.list.pop()
            player.move_star()
            player.set_limits()

    def planet_deck_start(self):
        ''' Load planet cards and assign self.planet_deck and deal starting cards'''
        self.planet_deck_dict = create_deck_dict(["blue","red", "purple", "green"])
        planet_deck_list = create_deck_list(self.planet_deck_dict)
        self.planet_deck = Deck(planet_deck_list)
        self.planet_deck.shuffle_deck()
        self.deal_cards(self.planet_deck,3)
    
    def star_deck_start(self):
        ''' Load cards, create star deck and assign stars to players'''
        self.star_deck_dict = create_deck_dict(["Star"])
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


    def correct_phase_for_planet(self):
        if self.turn_manager.phase in [ "first_planet" ,"creation_phase" ]:
            return True
        else:
            return False

    def planet_played(self,owner):
        ''' Check if player has created a planet this turn'''
        if self.players[owner].player_created == True:
                return True
        else:
            return False



    def planet_limit(self,card:Card,owner:int):
        ''' Check if planet wanting to be played is within stars limit'''
        planet_type = card.planet_type
        planet_limits  = self.players[owner].planet_limits 
        if planet_limits[planet_type] > self.players[owner].galaxy_planets_sum(type=planet_type):
            return True
        else:
            return False


    def check_allowed_planet_play(self,card:Card,owner:int):
        ''' check if planet is allowed to be played'''
        if self.correct_phase_for_planet():
            if not self.planet_played(owner): 
                if self.planet_limit(card,owner):

                    return True
        else:
            return False

    def clicked_card(self, card, owner:int):
        ''' What to do when a card is clicked'''

        if card.card_type == "planet":
            
            allowed = self.check_allowed_planet_play(card,owner)
            if allowed:
                player = self.players[owner]

                if card in player.hand:
                    self.play_planet(player, card)
                elif card in player.galaxy:
                    pass
            else:
                pass #print("cant do that ")

    def next_phase(self):
        ''' Self moves to the next turn'''
        self.turn_manager.next_phase(self.players)

        if self.turn_manager.phase == "draw_phase":
            self.deal_cards(self.planet_deck,1)