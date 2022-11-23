def draw_x_planets(gm,card,n):
    for x in range(0,n):
        gm.deal_card(gm.planet_deck,card.owner)

effect_dict = {
    "green10b" : {"function" : draw_x_planets, "args" : [1]}
}