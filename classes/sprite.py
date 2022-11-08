import pygame
class Sprite(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y,location, card_type) -> None:
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = self.load_and_rescale(location,card_type)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]
        self.update()
        
    def load_and_rescale(self,location:str, card_type:str):
        image = pygame.image.load(location)
        if card_type == "star":
            image = pygame.transform.scale(image, (int(195), int(225))) #165, 225
        else:
            image = pygame.transform.scale(image, (int(165), int(225))) #165, 225
        return image
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self,x:int,y:int):
        self.pos_x = x
        self.pos_y = y
        self.update()
    
    def update(self):
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 165, 225)