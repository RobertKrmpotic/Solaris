class TurnManager:
    def __init__(self):
        self.player_turn=1
        self.turn_n = 0
        self.phase = "pre_game_setup"
        self.standard_phases= [
            "draw_phase"
            "creation_phase",
            "main_phase",
            "lure_phase",
            "invasion_phase"
        ]
        self.pregame_phases = [ "pre_game_setup",
         "discard_phase",
         "first_planet"]
        



    def next_phase(self,players):
        ''' moves to the next phase'''

        if self.phase =="pre_game_setup":
            self.phase = "discard_phase"

        elif self.phase =="discard_phase":
            self.phase = "first_planet"
        
        elif self.phase =="first_planet":
            for player in players.values():
                player.reset_planet_created()
            self.turn_n += 1
            self.phase = "draw_phase"
        
        #standard loop
        elif self.phase =="draw_phase":
            self.phase = "creation_phase"
        
        elif self.phase =="creation_phase":
            self.phase = "main_phase"
        
        elif self.phase =="main_phase":
            if self.player_turn ==1:
                self.player_turn =2
            else:
                self.phase = "lure_phase"
                self.player_turn = 1

        elif self.phase =="lure_phase":
            self.phase = "invasion_phase"
        
        elif self.phase =="invasion_phase":
            if self.player_turn ==1:
                self.player_turn =2
            else:
                for player in players.values():
                    player.reset_planet_created()
                    player.reset_mana()
                self.turn_n +=1
                self.phase = "draw_phase"
                self.player_turn = 1

