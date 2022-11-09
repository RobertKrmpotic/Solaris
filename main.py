import yaml
import pygame
import glob
from classes.card import Card
from classes.deck import Deck
from classes.game_manager import GameManager


def renderGame(window,background,visible_cards,button, phase, player_turn):
    window.blit(background, ( 0,0))
    font = pygame.font.SysFont('Roboto',45, True)
    for card in visible_cards:
        card.sprite.draw(window)


    RED = (255, 255, 255)
    pygame.draw.rect(window, RED, button)
    # You can pass the center directly to the `get_rect` method.
    text_surf = font.render(f"phase :{phase}, player: {player_turn}", True, RED)
    text_rect = text_surf.get_rect(center=(1200/2, 630))
    window.blit(text_surf, text_rect)
    pygame.display.update()

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
        #for card in player.hand:
            #gm.visible_cards.append(card)
            #sprites.add(card.sprite)

    while run:
        key = None 
        gm.sort_hands()
        button = pygame.Rect(0, 100, 100, 100)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                key = event.key
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    if button.collidepoint(event.pos):
                        gm.next_phase()
                

                clicked_cards = [c for c in gm.visible_cards if c.sprite.rect.collidepoint(pos)]
                for card in clicked_cards:
                    gm.clicked_card(card, card.owner)
                
                

        renderGame(window,background, gm.visible_cards, button,gm.turn_manager.phase, gm.turn_manager.player_turn)

main()