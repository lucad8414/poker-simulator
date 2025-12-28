from card import Cards
from enum import Enum

class States(Enum):
    Flop = 0
    Turn = 1
    River = 2

class Board:
    def __init__(self, cards: list[Cards]):
        self.cards = cards
        self.state: States = States.Flop

        assert len(self.cards) == 3
        

    def run(self, card: Cards):
        match self.state:
            case States.Flop:
                self.state = States.Turn
                self.cards.append(card)
                assert len(self.cards) == 4
                

            case States.Turn:
                self.state = States.River
                self.cards.append(card)
                assert len(self.cards) == 5
                

            case River:
                raise ValueError("Five cards on the Board, should not draw now!")

