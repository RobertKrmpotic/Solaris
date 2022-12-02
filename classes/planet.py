from classes.card import Card
from classes.planet_buff import Buff
class Planet(Card):
    def __init__(self, *initial_data, **kwargs):
        super().__init__(*initial_data, **kwargs)
        self.treasure_dict = self.sum_treasure()
        self.original_dmg = self.damage
        self.destructable = True
        self.buffs = {} #dict might be better [{"amount":0, }, {}]
        self.debuffs = {}
    
    def sum_treasure(self):
        return {"water" : self.treasure_water,
            "rock" : self.treasure_rock,
            "cloud" :  self.treasure_cloud,
            "plutonium" : self.treasure_plutonium}

    def sum_buffs(self):
        total_buff = 0
        for key,buff in self.buffs.items():
            if buff.active:
                total_buff += buff.amount
        return total_buff
    def recalculate_damage(self):
        ''' Calculate total damage including buffs and debuffs'''
        buffs = self.sum_buffs()
        self.damage = self.original_dmg +  buffs #- sum(self.debuffs)
    