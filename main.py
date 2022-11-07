import yaml
import pygame
import glob
from classes.card import Card
from classes.deck import Deck
from classes.game_manager import GameManager


def renderGame(window,background,visible_cards):
    window.blit(background, ( 0,0))
    font = pygame.font.SysFont('comicsans',60, True)
    for card in visible_cards:
        card.sprite.draw(window)

def main():
    pygame.init()
    bounds = (1900, 1200)
    window = pygame.display.set_mode(bounds)

    pygame.display.set_caption("Solaris")
    run = True
    background = pygame.image.load('assets/background/galaxy.jpg')
    #sprites = pygame.sprite.Group() #probably should be part of gm
    gm = GameManager()

    for player in gm.get_players():
        gm.visible_cards.append(player.star)
        for card in player.hand:
            gm.visible_cards.append(card)
            #sprites.add(card.sprite)

    while run:
        key = None 
        gm.sort_hands()
        renderGame(window,background, gm.visible_cards)
        #sprites.draw(window)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                key = event.key
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                gm.next_phase()
                
                clicked_cards = [c for c in gm.visible_cards if c.sprite.rect.collidepoint(pos)]
                for card in clicked_cards:
                    if card.card_type == "planet":
                        print(card.sprite.pos_x)
                        #gm.play_planet(gm.player2, card)
                        gm.visible_cards.remove(card)
        
    

main()