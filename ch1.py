# OOD Ch 1
import random

# implementing __init__() in a supercalss
# Card supercalss and its three subclasses
class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
        self.hard, self.soft = self._points()
class NumberCard(Card):
    def _points(self):
        return int(self.rank), int(self.rank)
class AceCard(Card):
    def _points(self):
        return 1, 11
class FaceCard(Card):
    def _points(self):
        return 10, 10

# implementing __init__() in each subclass
# some redundency in subclass __init__()
##class Card:
##    pass
##class NumberCard(Card):
##    def __init__(self, rank, suit):
##        self.suit = suit
##        self.rank = str(rank)
##        self.hard = self.soft = rank
##class AceCard(Card):
##    def __init__(self, rank, suit):
##        self.suit = suit
##        self.rank = 'A'
##        self.hard, self.soft = 1, 11
##class FaceCard(Card):
##    def __init__(self, rank, suit):
##        self.suit = suit
##        self.rank = {11: 'J', 12: 'Q', 13: 'K'}[rank]
##        self.hard = self.soft = 10
# pull redundency up to superclass, more complexity compared
# to implementing __init__() in a supercalss
##class Card:
##    def __init__(self, rank, suit, hard, soft):
##        self.rank = rank
##        self.suit = suit
##        self.hard = hard
##        self.soft = soft
##class NumberCard(Card):
##    def __init__(self, rank, suit):
##        super().__init__(str(rank, suit, rank, rank))
##class AceCard(Card):
##    def __init__(self, rank, suit):
##        super().__init__("A", suit, 1, 11)
##class FaceCard(Card):
##    def __init__(self, rank, suit):
##        super().__init__({11: 'J', 12: 'Q', 13: 'K'}[rank], suit, 10, 10)
# above implementation simplifies factory function
def card10(rank, suit):
    if rank == 1: return AceCard(rank, suit)
    elif 2 <= rank < 11: return NumberCard(rank, suit)
    elif 11 <= rank < 14: return FaceCard(rank, suit)
    else:
        raise Exception("Rank our of range")
'''
NOTE:
trade-off between complext __init__() and factory function
often better to stick with more direct __init__() and push
complexity into factory funciton
'''

# class used to build four manifest constants
class Suit:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

[Club, Diamond, Heart, Spade] = [Suit('Club', '♣'), Suit('Diamond', '♦'),
                                 Suit('Heart', '♥'), Suit('Spade', '♠')]

cards = [AceCard('A', Spade), NumberCard('2', Spade),
        NumberCard('3', Spade)]

# factory functions for various Card subclass
def card(rank, suit):
    if rank == 1: return AceCard('A', suit)
    elif 2 <= rank < 11: return NumberCard(str(rank), suit)
    elif 11 <= rank < 14:
        name = {11: 'J', 12: 'Q', 13:'K'}[rank]  # use mapping insead of a chain of elif in simple condition
        return FaceCard(name, suit)
    else:  # be explicit and use else to raise exception
        raise Exception("Rank out of range")

def card4(rank, suit):  # use mapping only, but rank is not a string 
    class_ = {1: AceCard, 11: FaceCard, 12: FaceCard,
              13: FaceCard}.get(rank, NumberCard)
    return class_(rank, suit)

def card5(rank, suit):  # parallel mapping, a repetition of the mapping keys, not desirable 
    class_ = {1: AceCard, 11: FaceCard, 12: FaceCard,
              13: FaceCard}.get(rank, NumberCard)
    rank_str = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}.get(rank, str(rank))
    return class_(rank_str, suit)
'''
NOTE:
two parallel structures should be replaced with tuple or a proper collection 
'''

def card6(rank, suit):  # use a two-tuple to replace paralle mapping
    class_, rank_str = {
        1: (AceCard, 'A'),
        11: (FaceCard, 'J'),
        12: (FaceCard, 'Q'),
        13: (FaceCard, 'K'),
        }.get(rank, (NumberCard, str(rank)))
    return class_(rank_str, suit)
d = [card6(r+1, 1) for r in range(13) for s in (Club,
            Diamond, Heart, Spade)]
random.shuffle(d)
hand = [d.pop(), d.pop()]

def card7(rank, suit):  # use partial function to map rank values to Card objects
    from functools import partial
    part_class = {
        1: partial(AceCard, 'A'),
        11: partial(FaceCard, 'J'),
        12: partial(FaceCard, 'Q'),
        13: partial(FaceCard, 'K'),
        }.get(rank, partial(NumberCard, str(rank)))
    return part_class(suit)
deck = [card7(rank, suit)
        for rank in range(1, 14)
        for suit in (Club, Diamond, Heart, Spade)]


class CardFactory:  # evaluating method sequentially instead of using partial funciton
    def rank(self, rank):
        self.class_, self.rank_str = {
            1: (AceCard, 'A'),
            11: (FaceCard, 'J'),
            12: (FaceCard, 'Q'),
            13: (FaceCard, 'K'),
            }.get(rank, (NumberCard, str(rank)))
        return self
    def suit(self, suit):
        return self.class_(self.rank_str, suit)
card8 = CardFactory()
deck8 = [card8.rank(r+1).suit(s) for r in range(13) for s in (Club,
            Diamond, Heart, Spade)]

# use composite object(container) to create a deck
# design strategy 1: Wrap
class Deck:
    def __init__(self):
        self._cards = [card6(r+1, 1) for r in range(13) for s in (Club,
            Diamond, Heart, Spade)]
        random.shuffle(self._cards)
    def pop(self):
        return self._cards.pop()
d = Deck()
hand = [d.pop(), d.pop()]
'''
NOTE:
A wrapper class contains methods that are delegated to the underlying
implementation class(pop() in above case).For a sophisticated collection,
a large number of methods may be delegated to the wrapper object.
'''
# design strategy 2: Extend
# to extend a built-in class, list in this case, so that Deck2 inherits pop()
class Deck2(list):
    def __init__(self):
        super().__init__(card6(r+1, 1) for r in range(13) for s in (Club,
            Diamond, Heart, Spade))
        random.shuffle(self)

# a class provides a collection of Card instances dealt from a shoe that
# has 1 or more 52 cards deck and a burn card
class Deck3(list):
    def __init__(self, decks=1):
        super().__init__()
        self.extend(card6(r+1, 1) for r in range(13) for s in (Club,
            Diamond, Heart, Spade) for d in range(decks))
        random.shuffle(self)
        burn = random.randint(1, 52)
        for i in range(burn): self.pop()

class Hand:
    def __init__(self, dealer_card):
        self.dealer_card = dealer_card
        self.cards = []
    def hard_total(self):
        return sum(c.hard for c in self.cards)
    def soft_total(self):
        return sum(c.soft for c in self.cards)

d = Deck()
h = Hand(d.pop())
h.cards.append(d.pop())
h.cards.append(d.pop())

# use start operator to enable building a composite object in a single statement
class Hand2:
    def __init__(self, dealer_card, *cards):
        self.dealer_card = dealer_card
        self.cards = list(cards)
    def hard_total(self):
        return sum(c.hard for c in self.cards)
    def soft_total(self):
        return sum(c.soft for c in self.cards)
# build Hand object with multiple statements of method evaluation
d = Deck()
h = Hand2(d.pop())
h.cards.append(d.pop())
h.cards.append(d.pop())
# build Hand object with single statement
d = Deck()
h = Hand2(d.pop(), d.pop(), d.pop())

# A stateless(no internal variables) Strategy object which will be plugged into
# a Player object, design Strategy object like a collection of methods
class GameStrategy:
    def insurance(self, hand):
        return False
    def split(self, hand):
        return False
    def double(self, hand):
        return False
    def hit(self, hand):
        return sum(c.hard for c in hand.cards) <= 17

