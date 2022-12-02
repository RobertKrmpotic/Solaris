from classes.planet_buff import Buff

#draw
def draw_x_planets(gm,card,n):
    for _ in range(0,n):
        gm.deal_card(gm.planet_deck,card.owner)

#buffs
def buff_itself(gm,card,buff_type:str,amount:int,effect_id:str):
    ''' Buff itself for a certain amount'''
    card.buffs[f"passive_{effect_id}"] = Buff(buff_type,amount, effect_id)
    card.recalculate_damage()

def bonus_for_every_rocky(gm, card, effect_id:str):
    ''' get bonus for yourself for every rocky planet in your system'''
    total_bonus = 0
    for planet in gm.players[card.owner].galaxy:
        if planet.planet_type == "rocky":
            total_bonus += 1
    buff_itself(gm,card, "passive" ,total_bonus,effect_id )
    
def bonus_if_n_planets(gm,card,n_planets:int, bonus_amount:int, effect_id:str):
    ''' get bonus if you have n planets or more in your galaxy'''
    total_buff = 0
    if len(gm.players[card.owner].galaxy) >= n_planets:
        total_buff += bonus_amount
    buff_itself(gm,card, "passive", total_buff, effect_id )

def buff_all_planet_types(gm,card,type:str,amount:int, effect_id:str):
    ''' buffs all certain planet types'''
    for planet in gm.players[card.owner].galaxy:
        if planet.planet_type == type:
            if planet == card:
                buff_itself(gm,planet, "passive" ,amount,effect_id ) 
            else:
                buff_itself(gm,planet, "passive_from_another" ,amount,effect_id ) #TODO figure of what types of effects should do

def discard_a_card(gm,card):
    ''' Discard a card from your hand'''
    print("discarding cards")
    card.once_per_turn = False

effect_dict = {
    "green10b" : {"function" : draw_x_planets, "args" : [1]},
    "blue6" : {"function" : discard_a_card, "args" : [] },
    "blue13b" : {"function" : bonus_for_every_rocky, "args" : ["blue13b"]},
    "blue12b" : {"function" : buff_itself, "args" : [] },
    "red1b" : {"function" : bonus_if_n_planets, "args" : [2,2,"red1b"]},
    "red13" : {"function" : buff_all_planet_types, "args" : ["rocky",2, "red13" ]},

}