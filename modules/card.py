import os
import cv2

class Card:
    """
    Creating an object for each card having the following attributes:
        Value: Face Value of the card
        Color: Corresponding to one of the 4 suits in a card deck
        Score: Score of the card in this game
        win_priority: priority of the card in deciding hand winner
        Validity: 1 if card is valid to play in that turn else 0
        img_path: local path of the image of the card
        card_img: img of the card in memory
    """
    def __init__(self, value, color, validity, score, win_priority):
        self.value = value
        self.color = color
        self.validity = validity
        self.score = score
        self.win_priority = win_priority
        self.img_path = "{}_of_{}.png".format(self.value.lower(), self.color.lower())
        self.card_img = cv2.imread(os.path.join(os.getcwd(), "modules/img/cards/", self.img_path))
        self.card_img = cv2.resize(self.card_img, (160,232))

    def __str__(self):
        """
        Reveals the requested card.
        """
        return "{rank} of {suit}".format(rank=self.value, suit=self.color)