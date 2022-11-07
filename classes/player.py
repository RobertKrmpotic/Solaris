class Player():
    def __init__(self, number:int):
        self.number = number
        self.current_move = False
        self.star = None
        self.power_played = False
        self.superpower_played = False
        self.hand = []
        self.hand_y = self.calc_hand_y()
        self.galaxy_y = self.calc_galaxy_y()
        self.discard_pile = []
        self.galaxy = [] #can be dict?
        self.entrance = []
        self.leaches = 0
        self.points = 0
        self.max_mana = 4
        self.mana = self.max_mana
    
    def calc_hand_y(self):
        if self.number == 1:
            return 50
        elif self.number ==2:
            return 900
    
    def calc_galaxy_y(self):
        if self.number == 1:
            return 300
        elif self.number ==2:
            return 650

    def move_star(self):
        ''' Move star to starting position'''
        x = 100
        self.star.sprite.move(x,self.galaxy_y)

    def sort_hand(self):

        if len(self.hand) >0:
            x = 400
            for card in self.hand:
                card.sprite.move(x,self.hand_y)
                x += 200
    
    def sort_galaxy(self):

        if len(self.hand) >0:
            x = 400
            for planet in self.galaxy:
                planet.sprite.move(x,self.galaxy_y)
                x += 200
