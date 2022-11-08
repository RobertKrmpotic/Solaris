from classes.sprite import Sprite
class Card():
    def __init__(self,*initial_data, **kwargs ):
        #set attributes from dictionary
        self.owner = None
        self.showcard = False
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
        
        self.sprite = Sprite(206, 281,200,200, self.image_location, self.card_type) #165, 225