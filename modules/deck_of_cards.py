import random
from modules.card import Card

class DeckOfCards(Card):

    def __init__(self):
        # Initializes a deck of card for 29 card game
        self.CARD_GUIDE = {  "Ace": {"Score": 1, "Win_Priority":3},
                "7": {"Score": 0, "Win_Priority":8},
                "8": {"Score": 0, "Win_Priority":7},
                "9": {"Score": 2, "Win_Priority":2},
                "10": {"Score": 1, "Win_Priority":4},
                "Jack": {"Score": 3, "Win_Priority":1},
                "Queen": {"Score": 0, "Win_Priority":6},
                "King": {"Score": 0, "Win_Priority":5}
            }
        self.COLORS = ['Heart', 'Diamonds', 'Spades', 'Clubs']
        self.contents = [Card(value, color, 1, self.CARD_GUIDE[value]["Score"], self.CARD_GUIDE[value]["Win_Priority"]) for value in list(self.CARD_GUIDE.keys()) for color in self.COLORS]

    def shuffleDeck(self):
        """
        Self-explanatory. Shuffles the deck.
        """
        for i in range(0, 3):
            random.shuffle(self.contents)

    def draw(self):
        """
        Draws a single card to a variable.
        Useful for replacing and discarding individual cards in a hand, such as replacing cards in poker.
        To do so: <hand>[<card to replace>] = cards.draw()
        Remember that the list for a hand starts from 0, not 1.
        """
        return self.contents.pop()

    def drawHand(self, size):
        """
        Draws a <size>-card hand from the deck.
        """
        return [self.draw() for i in range(0, size)]

    def dealCards(self, player_list):
        for player in player_list:
            player.hand = player.hand + self.drawHand(4)

    def __str__(self):
        return "Deck has {deck_size} cards".format(deck_size=len(self.contents))