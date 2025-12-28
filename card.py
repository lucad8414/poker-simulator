from card_types import Values, Symbols


class Cards:
    def __init__(self, value: Values, symbol: Symbols):
        self.value = value
        self.symbol = symbol

        self.power: int = 0
        if self.value.value.isnumeric():
            self.power = int(self.value.value)

        else:
            if self.value == Values.Jack:
                self.power = 11
            elif self.value == Values.Queen:
                self.power = 12
            elif self.value == Values.King:
                self.power = 13
            elif self.value == Values.Ace:
                self.power = 14
            else:
                # only Dummy left:
                self.power = 100

        assert self.power != 0


    def __leq__(self, other: "Cards") -> bool:
        
        return self.power <= other.power
        

