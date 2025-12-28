from card import Cards
from card_types import Values, Symbols
import random


class Deck:
    def __init__(self):
        self.cards: list[Cards] = []

        for value in Values:
            for symbol in Symbols:
                self.cards.append(Cards(value, symbol))

        assert len(self.cards) == 52


    def deal(self) -> Cards:
        if len(self.cards) == 0:
            raise ValueError("Can't deal no more cards, Deck is empty.")
        return self.cards.pop(random.randint(0, len(self.cards) - 1))
        
