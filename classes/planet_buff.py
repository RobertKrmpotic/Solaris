class Buff():
    def __init__(self,type, amount,effect_id) -> None:
        self.type = type
        self.amount = amount
        self.effect_id = effect_id
        self.active = True
