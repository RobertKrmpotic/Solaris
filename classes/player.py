class Player():
    def __init__(self, number:int):
        self.number = number
        self.current_move = False
        self.star = None
        self.planet_limits = {}
        self.power_played = False
        self.player_created = False
        self.superpower_played = False
        self.hand = []
        self.hand_y = self.calc_hand_y()
        self.galaxy_y = self.calc_galaxy_y()
        self.discard_pile = []
        self.galaxy = [] #can be dict?
        self.entrance = []
        self.leaches = []
        self.leach_count = 0
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

    def sort_invaders(self):
        ''' Sort invader sprites'''
        x = 900
        for invader in self.entrance:  
            invader.sprite.move(x,self.galaxy_y-50)
            x += 200

    def sort_hand(self):

        if len(self.hand) >0:
            x = 400
            for card in self.hand:
                card.sprite.move(x,self.hand_y)
                x += 200
    
    def sort_galaxy(self):
        ''' Sort galaxy to have good x'''
        if len(self.galaxy) >0:
            x = 300
            for planet in self.galaxy:
                
                planet.sprite.move(x,self.galaxy_y)
                x += 200
    
    def galaxy_planets_sum(self,type:int):
        ''' gets a sum of types of planets'''
        sum = 0
        for planet in self.galaxy:
            if planet.planet_type == type:
                sum +=1
        return sum

    def reset_mana(self):
        self.mana = self.max_mana
    
    def reset_planet_created(self):
        self.player_created = False
    
    def set_limits(self):
        ''' sets a dict with planet limits'''
        limit_dict = {}
        limit_dict["gas"] = self.star.limit_gas
        limit_dict["water"] = self.star.limit_water
        limit_dict["rocky"] = self.star.limit_rocky
        limit_dict["dwarf"] = self.star.limit_dwarf
        self.planet_limits = limit_dict

    def sum_treasure(self, element):
        ''' Sum total of a specific types of treasure'''
        total_treasure = 0
        for planet in self.galaxy:
            total_treasure += planet.treasure_dict[element]
        return total_treasure

