import yaml
import glob

from classes.player import Player
from classes.deck import Deck
from classes.card import Card
from classes.turn_manager import TurnManager

from classes.utils import create_deck_dict, create_deck_list
from classes.effects import effect_dict
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
        self.invader_deck = []
        self.star_deck = []
        self.pre_start()
    

    #BASICS
    def get_players(self):
        return [self.player1, self.player2]

    def switch_lists(self,card:Card,from_list:list, to_list:list):
        ''' Takes a card from one list and append it to the other '''
        to_list.append(card)
        from_list.remove(card)
    
    def deal_card(self,deck:Deck, owner:int):
        ''' deal a card from the deck to a player hand'''
        card = deck.list.pop()
        card.owner = owner
        self.players[owner].hand.append(card)
        self.visible_cards.append(card)

    def deal_cards(self,deck, n):
        ''' deal n cards from the deck to each players hand'''
        for _ in range(0,n):
            self.deal_card(deck,1)
            self.deal_card(deck,2)

    def pre_start(self):
        ''' do a setup for turn 0'''
        self.planet_deck_start()
        self.star_deck_start()
        self.invader_deck_start()
        
    def sort_hands(self):
        ''' Sorts correct position of sprites in hand'''
        for player in self.get_players():
            player.sort_hand()

    def clicked_card(self, card:Card, owner:int):
        ''' What to do when a card is clicked'''
        if card.card_type == "planet":
            allowed_building = self.check_allowed_planet_play(card,owner)
            allowed_effect = self.check_allowed_effect(card,owner)
            if allowed_building:
                player = self.players[owner]
                if card in player.hand:
                    self.play_planet(player, card)
            if allowed_effect:
                player = self.players[owner]
                if card in player.galaxy:
                    effect = effect_dict[card.id]
                    effect["function"](self,card,*effect["args"])
                    print("effect")
            else:
                pass 
        self.recalculate_galaxy_damage()

    def next_phase(self):
        ''' Self moves to the next turn'''
        self.turn_manager.next_phase(self.players)

        if self.turn_manager.phase == "draw_phase":
            self.deal_cards(self.planet_deck,1)
            self.invaders_to_limbo(self.invader_deck,2)
        
        if self.turn_manager.phase == "lure_phase":
            self.lure_invaders()
        if self.turn_manager.phase == "invasion_phase":
            self.invade_galaxy(self.turn_manager.player_turn)

            pass
        

    # STAR
    def star_deck_start(self):
        ''' Load cards, create star deck and assign stars to players'''
        self.star_deck_dict = create_deck_dict("stars")
        star_deck_list = create_deck_list(self.star_deck_dict)
        self.star_deck = Deck(star_deck_list)
        self.star_deck.shuffle_deck()
        self.assign_stars()

    def assign_stars(self):
        ''' assign a star to each player'''
        for player in self.get_players():
            player.star = self.star_deck.list.pop()
            player.move_star()
            player.set_limits()
    
    def recalculate_galaxy_damage(self):
        ''' Refreshes card damage'''
        for player in self.players.values():
            for planet in player.galaxy:
                for key,buff in planet.buffs.items():
                    if buff.type == "passive":
                        effect = effect_dict[planet.id]
                        effect["function"](self,planet,*effect["args"])
                planet.recalculate_damage()
                print(f"planet: {planet.name}, damage: {planet.damage}")
    # Invaders

    def sort_limbo(self):
        ''' Sorts position of invaders in the limbo'''
        limbo_y = 600
        limbo_x = 1200
        for invader in self.limbo:
            invader.sprite.move(limbo_x,limbo_y)
            limbo_x += 200

    def invaders_to_limbo(self,deck:Deck,n:int):
        ''' Send invaders from invaders deck to limbo'''
        for _ in range(0,n):
            card = deck.list.pop()
            self.limbo.append(card)
            self.sort_limbo()
            self.visible_cards.append(card)

    def invader_deck_start(self):
        ''' Load invader cards into a deck'''
        self.invader_deck_dict = create_deck_dict("invaders")
        invader_deck_list = create_deck_list(self.invader_deck_dict)
        self.invader_deck = Deck(invader_deck_list)
        self.invader_deck.shuffle_deck()

    def lure_invaders(self):
        ''' Send invaders to needed entrances of galaxies'''
        switch_list = []
        for invader in self.limbo:
            element = invader.attracted_to
            element_total = {}
            for player in self.players:
                element_total[player] = self.players[player].sum_treasure(element)
            if element_total[1] != element_total[2]:
                top_player = max(element_total, key=element_total.get)
                to_append = (invader,top_player)   
                switch_list.append(to_append)
                
        for item in switch_list:
            #item 0 is invader
            self.switch_lists(item[0], self.limbo, self.players[item[1]].entrance)
        for player in self.players:
            self.players[player].sort_invaders()

    def invade_galaxy(self, player_n:int):
        ''' Invade galaxy of a player and walk invaders through planets'''
        player = self.players[player_n]
        to_discard = []
        to_leach = []
        for invader in player.entrance:
            for planet in reversed(player.galaxy):
                invader.hp -= planet.damage
                if invader.hp <= 0:
                    to_discard.append(invader)
                    break
            if invader.hp >0:
                to_leach.append(invader)
            self.visible_cards.remove(invader)
        
        for invader in to_discard:
            self.switch_lists(invader,player.entrance, player.discard_pile)
        for invader in to_leach:
            self.switch_lists(invader,player.entrance, player.leaches)

    # PLANET
    def planet_deck_start(self):
        ''' Load planet cards and assign self.planet_deck and deal starting cards'''
        self.planet_deck_dict = create_deck_dict("planets")
        planet_deck_list = create_deck_list(self.planet_deck_dict,"planet")
        self.planet_deck = Deck(planet_deck_list)
        self.planet_deck.shuffle_deck()
        self.deal_cards(self.planet_deck,3)

    def correct_phase_for_planet(self):
        ''' Check if planet building is allowed in this phase'''
        if self.turn_manager.phase in [ "first_planet" ,"creation_phase" ]:
            return True
        else:
            return False
    

    def planet_played(self,owner:int):
        ''' Check if player has created a planet this turn'''
        if len(self.players[owner].planet_played_this_turn) > 0:
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
    
    def check_allowed_effect(self,card:Card,owner:int):
        ''' check if planet is allowed to be played'''
        if self.turn_manager.phase in [ "main_phase" ]:
            if hasattr(card, 'once_per_turn'):
                if card.once_per_turn:
                    return True
        else:
            return False

    def play_once_created_effect(self,player):
        ''' check if once created effect neeeds to be played'''
        card = player.planet_played_this_turn[-1]
        if card.once_created:
            effect = effect_dict[card.id]
            effect["function"](self,card,*effect["args"])
            print()
            print("once created")

    def play_planet(self, player:Player, planet:Card):
        ''' Take a planet from players hand and put it in their galaxy'''
        self.switch_lists(planet, player.hand, player.galaxy)
        player.planet_played_this_turn.append(planet)
        player.sort_hand()
        player.sort_galaxy()
        self.play_once_created_effect(player)
        print(planet.damage)
