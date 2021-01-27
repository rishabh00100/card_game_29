class Card:
    """
    Creating an object for each card having the following attributes:
        Value: Face Value of the card
        Color: Corresponding to one of the 4 suits in a card deck
        Score: Score of the card in this game
        win_priority: priority of the card in deciding hand winner
        Validity: 1 if card is valid to play in that turn else 0
    """
    def __init__(self, value, color, validity, score, win_priority):
        self.value = value
        self.color = color
        self.validity = validity
        self.score = score
        self.win_priority = win_priority

    def __str__(self):
        """
        Reveals the requested card.
        """
        return "{rank} of {suit}".format(rank=self.value, suit=self.color)