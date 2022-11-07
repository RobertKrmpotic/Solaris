import pygame
class Sprite(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y,location) -> None:
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = self.load_and_rescale(location)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]
        self.update()
        
    def load_and_rescale(self,location):
        image = pygame.image.load(location)
        image = pygame.transform.scale(image, (int(165), int(225)))
        return image
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self,x:int,y:int):
        self.pos_x = x
        self.pos_y = y
        self.update()
    
    def update(self):
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 165, 225)