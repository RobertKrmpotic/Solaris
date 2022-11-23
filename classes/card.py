from classes.sprite import Sprite
class Card():
    def __init__(self,*initial_data, **kwargs ):
        #set attributes from dictionary
        self.owner = None
        self.showcard = False
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        #for key in kwargs:
        #    setattr(self, key, kwargs[key])
        self.treasure_dict = self.sum_treasure()
        self.add_attributes()
        self.sprite = Sprite(206, 281,200,200, self.image_location, self.card_type) #165, 225
    
    def sum_treasure(self):
        if self.card_type == "planet":
            return {"water" : self.treasure_water,
             "rock" : self.treasure_rock,
             "cloud" :  self.treasure_cloud,
             "plutonium" : self.treasure_plutonium}
    
    def add_attributes(self):
        if self.card_type == "planet":
            self.destructable = True
            self.buffs = 0 #dict might be better
            self.debuffs = 0

