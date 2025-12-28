from card import Cards
from card_types import Values, Symbols
from hand import Hand
from board import Board
from deck import Deck
from enum import Enum


# ----------------------------------------------------------------------------


class Result(Enum):
    HighCard = 0
    Pair = 1
    TwoPair = 2
    Triple = 3
    Straight = 4
    Flush = 5
    FullHouse = 6
    Quads = 7
    StraightFlush = 8
    RoyalFlush = 9


# ----------------------------------------------------------------------------


def summs(cards: list[Cards]) -> dict[Values, int]:
    """
    Computes the amount of occurances of every Card value and returns in a key, 
    value pair dictionary, with cards.value and amount.
    """
    amounts: dict[Values, int] = {}
    
    for card in cards:
        if card.value in amounts.keys():
            amounts[card.value] += 1
        else:
            amounts[card.value] = 1
    
    return amounts


# ----------------------------------------------------------------------------


def sort_cards(cards: list[Cards]) -> list[Cards]:
    """
    Sorts the cards with the overwritten leq comparison and internal power
    member. Returns ascendingly sorted list.
    Used for computing straights.
    """
    result = []
    
    while len(cards) > 0:

        smallest = Cards(Values.Dummy, Symbols.Spade)
        # Dummy has the highest value, so will be overwritten by every card.
        delete = -1 # index for removal of current smallest element.

        for index, card in enumerate(cards):
            if card <= smallest: # overwritten leq operator.

                # remember current smallest in list and its index.
                smallest = card
                delete = index
        
        # remove current smallest for future iterations and add to result.
        result.append(smallest)
        cards.remove(delete)

        # should not happen, but guarded, to prevent future problems.
        assert delete != -1
    
    return result


# ----------------------------------------------------------------------------


def check_straight(cards: list[Cards]) -> list[Cards]:
    """
    Check for any straight in the cards, meaning at least 5 in a row.
    Returns all the cards particapaiting in the straight.
    If the list is empty, means there is no straight.
    """
    # Sort the cards ascendingly.
    cards = sort_cards(cards)
    
    prev_max = 1 # maximum reached straight.
    straight = 1 # counts the back to back cards.
    prev_power = cards[0].power # first cards power. 
    end_index = 0 # ending index of the straight.
    
    for i, card in enumerate(cards[1:]):
        
        # the current cards power is exactly one more the the previous.
        # this means those are back to back cards.
        if card.power - 1 == prev_power:
            straight += 1
        
        # Special case, when we habe a pair in the middle, does not 
        # increase the straight, but doesnt break it as well.
        elif card.power == prev_power:
            pass

        # The distance between the two cards is at least two.
        else:
            # we change prev_max if we reached a higher straight or equal.
            # because of ascending sort that means, that a new equal straight is a
            # higher straight.
            # we remember how long out straight was and where it ended.
            # we end with plus one, because we dont iterate from 0.
            prev_max = straight
            end_index = i + 1 if straight >= prev_max else end_index
            straight = 1
        
        # always get the new power.
        prev_power = card.power
    
    # Special case, if the straight is Ace, 2, 3, 4, 5.
    if straight == 4 and cards[end_index].power == 5:
        if cards[-1].value == Symbols.Ace:
            return [cards[-1]] + [cards[:end_index]]
    
    # normal case, return all, even though we only count 5.
    # Higher one wins, but lower one could be a flush, so give all.
    elif straight >= 5:
        return cards[end_index - straight : end_index]
    
    # no straight, so empty list.
    else:
        return []

# ----------------------------------------------------------------------------


def get_keys(value: int, source: dict[Values, int]) -> list[Values]:
    """
    Basic search function for a dictionary, in this case called source. 
    Returns all the keys, which have the value == value.
    """

    res = []
    for key, val in source.items():
        if val == value:
            res.append(key)

    return res


# ----------------------------------------------------------------------------


def transform(reference: list[Values], target: list[Cards], sort: bool = True) -> list[Cards]:
    """
    Filters all the wanted cards from the target list, which are wished by reference.
    If sort, then we already return the sorted version (ascending).
    """

    res = []
    for t in target:
        if t.value in reference:
            res.append(t)
    
    if sort:
        res = sort_cards(res)

    return res


# ----------------------------------------------------------------------------


def check_flush(cards: list[Cards]) -> list[Cards]:
    """
    Checks if the cards hold a flush.
    Simple, just checking for symbols.
    """
    
    # save the different symbols
    heart = []
    spade = []
    diamond = []
    club = []

    for card in cards:
        if card.symbol == Symbols.Heart:
            heart.append(card)
        elif card.symbol == Symbols.Spade:
            spade.append(card)
        elif card.symbol == Symbols.Diamond:
            diamond.append(card)
        else:
            club.append(card)
    
    result = [heart, spade, diamond, club]
    
    # check for flush.
    for l in result:
        if len(l) >= 5:
            return l

    # No Flush.
    return []


# ----------------------------------------------------------------------------


def compare_pairs(c1: list[Cards], c2: list[Cards]) -> tuple[bool, tuple[list[Cards], list[Cards]]]:
    """
    Compars two pairs of any length, but has to be the same. Returns the two pairs dexcendingly sorted and a boolean, which tells you if they are equal or not.
    """

    # shouldnt compare different size pairs.
    assert len(c1) == len(c2)

    # both list should only be pairs.
    assert all(c1[0].value == x.value for x in c1[1:])
    assert all(c2[0].value == x.value for x in c2[1:])

    # pairs are equal.
    if c1[0].value == c2[0].value:
        
        return (True, (c1, c2))

    # overwritten leq.
    # but equal should not be possible, so it is less.
    elif c1[0] <= c2[0]:

        return (False, (c2, c1))
    
    # c1 > c2:
    else:

        return (False, (c1, c2))


# ----------------------------------------------------------------------------

    
def evaluate(board: Board, hand: Hand) -> tuple[Result, tuple[list[Cards], list[Cards]]]:
    
    # TODO: Probably best to do: (Result.value, ([eval_cards], [rest_cards]))
        
    c = board.cards
    c.append(hand[0])
    c.append(hand[1])

    hits = summs(c)

    hit = list(hits.values())
    hit.sort(reverse=True)
    
    result = Result.HighCard
    
    # TODO: Always keep the highest cards, so we have 5 to evaluate.
    eval_cards = []
    rest_cards = []

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    if hit[0] == 4 and result.value <= Result.Quads.value:

        result = Result.Quad # assign the result.
        eval_cards = transform(get_keys(4,hits),c) # get all the cards with the Value
        # which has the quads.
        
        # Get the highest cards from the rest.
        tmp = []
        for card in c:
            
            # All cards not in the Quad.
            if card.value != eval_cards[0].value:
                tmp.append(card)
        
        # Sort ascending.
        tmp = sort_cards(tmp)

        # take the last, so the highest.
        rest_cards = [tmp[-1]]

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    elif hit[0] == 3 and hit[1] >= 2 and result.value <= Result.FullHouse.value:
        result = Result.FullHouse
        
        # Special case with 3,3 Full House.
        if hit[1] == 3:
            # get a list of len 6
            tmp = transform(get_keys(3,hits),c)

            assert len(tmp) == 6

            # sort the list:
            # should now be card A, with A < B and B, so [A,A,A,B,B,B].
            tmp = sort_cards(tmp)
            
            # remove the first element, because the A triple is the smaller one.
            # And the strongest Full House is BBBAA.
            tmp = tmp[1:]
            
            # turn it around for clearness.
            eval_cards = list(reversed(tmp))
            

        # Special case with 3,2,2.
        elif hit[2] == 2:

            # get a list of len 4.
            tmp = transform(get_keys(2,hits),c) # all cards, with amount two.

            assert len(tmp) == 4

            # now same like other special case:
            # Should be [A,A,B,B] now with A < B.
            tmp = sort_cards(tmp)
            
            # We only need the higher pair, so we take the two Bs.
            eval_cards = transform(get_keys(3),c)
            eval_cards.append(tmp[2:])

        # Normal Full House, we only have 3,2,1,1:
        else:

            # just add the 3 and two.
            eval_cards = transform(get_keys(3,hits),c)
            eval_cards.append(transform(get_keys(2,hits),c))
        
        
        # all Full Houses have five cards, so no rest.
        rest_cards = []

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    elif hit[0] == 3 and result.value <= Result.Triple.value:
        result = Result.Triple

        eval_cards = transform(get_keys(3,hits),c)

        # Should only be able two be 3,1,1,1,1.
        
        tmp = transform(get_keys(1,hits),c)

        tmp = sort_cards(tmp)
        # get the two largest.
        rest_cards = [tmp[-1], tmp[-2]]
        
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    elif hit[0] == 2 and hit[1] == 2 and result.value <= Result.TwoPair.value:
        result = Result.TwoPair
        # TODO: Special case with 2,2,2
        
        eval_cards = transform(get_keys(2,hits),c)
        # Now the list is [A,A,B,B,C,C] where A < B < C.
        eval_cards = sort_cards(eval_cards)

        # Special case 2,2,2
        if len(eval_cards) == 6:
            
            tmp = transform(get_keys(1,hits),c)
            
            # we now add the AA to tmp
            tmp.append(eval_cards[:2])
            
            tmp = sort_cards(tmp)
            
            # largest element to the rest.
            rest_cards = [tmp[-1]]
                                    
            # only take the larger eval:
            eval_cards = eval_cards[2:]

        # The Structure 2,2,1,1,1
        else:
            
            tmp = transform(get_keys(1,hits),c)

            tmp = sort_cards(tmp)

            rest_cards = [tmp[-1]]

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    elif hit[0] == 2 and result.value <= Result.Pair.value:
        result = Result.Pair
        
        # should only be one pair:
        eval_cards = transform(get_keys(2,hits),c)

        assert len(eval_cards) == 2

        # get all remaining cards
        tmp = transform(get_keys(1,hits),c)
        
        # get the 3 highest cards.
        tmp = sort_cards(tmp)
        rest_cards = list(reversed(tmp))[:3]

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    elif hit[0] == 1 and result.value <= Result.HighCard.value:
        result = Result.HighCard
        
        # get board plus hand:
        tmp = sort_cards(c)
        
        # get the five highest cards.
        eval_cards = list(reversed(tmp))[:5]

        # no rest, because all are rest, just a convention of mine.
        rest_cards = []

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    # remember what we achieved in case of royal/ straight flush
    flush = False
    straight = False
    
    # get the straight and flush cards if it exists:
    st = []
    fl = []

    # if list is not empty we got a straight.
    if check_straight(c):
        st = check_straight(c)
        straight = True

        # we check anyway, for straight/royal flush, but only assign if
        # we did not get better stuff before.
        if result.value <= Result.Straight.value:
            eval_cards = st
            rest_cards = []
            result = Result.Straight
            
            # only take the highest part of the straight.
            if len(eval_cards) == 6:
                eval_cards = eval_cards[1:]

            elif len(eval_cards) == 7:
                eval_cards = eval_cards[2:]

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # same for flush
    if check_flush(c):
        fl = check_flush(c)
        flush = True

        # we update our result in case of no better option:
        if result.value <= Result.Flush.value:
            eval_cards = fl
            rest_cards = []
            result = Result.Flush

            # get the highest flush
            eval_cards = sort_cards(eval_cards)
    
            if len(eval_cards) == 6:
                eval_cards = eval_cards[1:]

            if len(eval_cards) == 7:
                eval_cards = eval_cards[2:]

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    # set straight_flush for royal flush.
    straight_flush = False

    
    # check for straight flush.
    if straight and flush:
        symb = fl[0].symbol
        back_to_back = 0
        max_combo = 0
        for card in st:
            if card.symbol == symb:
                back_to_back += 1
            else:
                if back_to_back >= max_combo:
                    # take care of special cases!!!!!
                    max_combo = back_to_back

        if max_combo >= 5 or back_to_back >= 5:
            # straight flush
            straight_flush = True
            result = Result.StraightFlush
    

    if straight_flush and st[-1].value == Values.Ace:
        result = Result.RoyalFlush
    
    return (result, (eval_cards, rest_cards))
    


# ----------------------------------------------------------------------------


def game(players: int):
    
    # You can play with 2 to 22 players, else it doesnt work.
    assert 2 <= players <= 22

    # initialize the deck
    deck = Deck()

    # draw one card:
    deck.deal()

    # deal the hands:
    hands: list[Hand] = []
    
    for _ in range(players):
        h = (deck.deal(), deck.deal())
        hands.append(h)

    # draw one card:
    deck.deal()

    # initialize the board:
    b: list[Cards] = [deck.deal() for _ in range(3)]
    board = Board(b)

    # draw one card:
    deck.deal()

    # draw the turn:
    board.run(deck.deal())

    # draw one card:
    deck.deal()

    # draw the river:
    board.run(deck.deal())

    return (board, hands)
    

# ----------------------------------------------------------------------------


