import random

COLORS = ['Heart', 'Diamonds', 'Spades', 'Clubs']
VALUES = ['Ace', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
MINIMUM_BET = 17
MAXIMUM_BET = 29
VALIDITY = 1

class Card:
    """Creating an object for each card
    has 2 attributes:
    Value = Face Value of the card
    Color = Corresponding to one of the 4 suits in a card deck
    Validity = 1 if card is valid to play in that turn else 0
    """
    def __init__(self, value, color, validity):
        self.value = value
        self.color = color
        self.validity = validity

    def flip(self):
        """
        Reveals the requested card.
        """
        print(self.cardName())

    def cardName(self):
        """
        Returns a string containing the card's name in common terms.
        """
        return "{rank} of {suit}".format(rank=self.value, suit=self.color)

    def cardScore(self):
        """
        Returns a string containing the card's name in common terms.
        """
        if self.value == 'Jack':
            score = 3
        elif self.value == '9':
            score = 2
        elif self.value == 'Ace':
            score = 1
        elif self.value == '10':
            score = 1
        else:
            score = 0
        return score

class DeckOfCards:

    def __init__(self):
        self.contents = []
        self.contents = [Card(value, color, VALIDITY) for value in VALUES for color in COLORS]

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

    def dealCards(self, PlayerSet):
        for player in PlayerSet:
            player.hand = player.hand + self.drawHand(4)
        return PlayerSet

class player(object):
    def __init__(self, name, bid, hand, score, bidpass):
        self.name = name
        self.hand = []
        self.bid = bid
        self.score = score
        self.bidpass = bidpass
    def getScore(self):
        return self.score
    def getHand(self):
        return  self.hand
    def printScore(self):
        print("Score of player: {score}".format(score = self.score))
    def showHand(self):
        size = len(self.hand)
        for i in range(0, size):
            self.hand[i].flip()
    def showHandToPlay(self):
        size = len(self.hand)
        for i in range(0, size):
            print("Press {i} for {card}".format(i = i, card = self.hand[i].cardName()))
    def getBet(self, Opponent_Bet):
        playerBet = -1
        while not playerBet in [range(0, MAXIMUM_BET+1)]:
            try:
                playerBet = int(input("%s Please input your bet between %s and %s or input 0 to pass/end betting:" %(self.name, Opponent_Bet + 1, MAXIMUM_BET)))
            except ValueError:
                """
                Error handling when input not an integer
                """
                print("That wasn't an integer :(")
            if playerBet == 0:
                validBet = True
                return playerBet
            elif playerBet <= Opponent_Bet:
                print('Invalid bet, please try again.')
            else:
                validBet = True
                return playerBet

    def isBidPass(self, playerBet):
        if playerBet == 0:
            return True
        else:
            return False

def setBid(Bid, BidderName):
    HigherBid = Bid
    HigherBidder = BidderName
    return HigherBid, HigherBidder

def isAllPlayerPass(PlayerSet, passCounter):
    if passCounter == len(PlayerSet):
        return True
    else:
        return False

def AllPlayerPassCondition(PlayerSet, PassCounter, HigherBid, HigherBidder):
    if isAllPlayerPass(PlayerSet, PassCounter):
        HigherBid, HigherBidder = setBid(MINIMUM_BET, PlayerSet[0].name)
        PlayerSet[0].bid = HigherBid
    else:
        HigherBid, HigherBidder = setBid(HigherBid, HigherBidder)
    return PlayerSet, HigherBid, HigherBidder

def incrementBidder(FirstBidder, SecondBidder, HigherBid):
    FirstBidder = FirstBidder
    SecondBidder = SecondBidder
    if FirstBidder < SecondBidder and HigherBid > 0:
        FirstBidder = SecondBidder + 1
    elif FirstBidder < SecondBidder and HigherBid == 0:
        FirstBidder = FirstBidder + 1
        SecondBidder = SecondBidder + 1
    elif FirstBidder > SecondBidder:
        FirstBidder = FirstBidder + 1
    return FirstBidder, SecondBidder

def BidExitCondition(PassCounter, HigherBid):
    if PassCounter >= 3 and HigherBid > 0:
        return True
    else:
        return False

def biddingModule(PlayerSet, FirstBidder, SecondBidder, newBid, PassCounter, HigherBidder, HigherBid, Bidder1High):
    while Bidder1High == True:
        newerBid, newerBidder = setBid(PlayerSet[FirstBidder].getBet(newBid), PlayerSet[FirstBidder].name)
        if PlayerSet[FirstBidder].isBidPass(newerBid):
            PassCounter = PassCounter + 1
            PlayerSet[FirstBidder].bidpass = True
            PlayerSet, HigherBid, HigherBidder = AllPlayerPassCondition(PlayerSet, PassCounter, HigherBid, HigherBidder)
            FirstBidder, SecondBidder = incrementBidder(FirstBidder, SecondBidder, HigherBid)
            if BidExitCondition(PassCounter, HigherBid):
                Bidder1High = False
                break
            HigherBid, HigherBidder, FirstBidder, SecondBidder, Bidder1High = biddingModule(PlayerSet, FirstBidder, SecondBidder,
                                                                                            newBid, PassCounter, HigherBidder,
                                                                                            HigherBid, Bidder1High)
        else:
            HigherBid, HigherBidder = setBid(newerBid, newerBidder)
            PlayerSet[FirstBidder].bid = HigherBid
            if HigherBid == MAXIMUM_BET:
                Bidder1High = False
                break
            HigherBid, HigherBidder, FirstBidder, SecondBidder, Bidder1High = biddingModule(PlayerSet, SecondBidder, FirstBidder,
                                                                                            newerBid, PassCounter, HigherBidder,
                                                                                            HigherBid, Bidder1High)
    return HigherBid, HigherBidder, FirstBidder, SecondBidder, Bidder1High


# print('***********STATUS AFTER VALID BID********')
# print('HigherBidder:', HigherBidder)
# print('HigherBid:', HigherBid)
# print('FirstBidder:', FirstBidder)
# print('SecondBidder:', SecondBidder)
# print('FirstBidder + SecondBidder:', (FirstBidder + SecondBidder))

def BiddingRound(PlayerSet):
    PassCounter = 0
    FirstBidder = 0
    SecondBidder = 1
    HigherBid = 0
    HigherBidder = PlayerSet[0].name
    Bidder1High = True
    HigherBid, HigherBidder, FirstBidder, SecondBidder, Bidder1High = biddingModule(PlayerSet, FirstBidder, SecondBidder,
                                                                                                  MINIMUM_BET, PassCounter, HigherBidder,
                                                                                                  HigherBid, Bidder1High)
    return HigherBid, HigherBidder

def DeclareBidWinner(Bid, BidderName, Team1):
    if BidderName in Team1:
        print("Team 1 won the betting round and will play to make %s points" % Bid)
        print("%s will set the trump" % BidderName)
        print("Team 2 has to make %s points to win" % (30 - Bid))
    else:
        print("Team 2 won the betting round and will play to make %s points" % Bid)
        print("%s will set the trump" % BidderName)
        print("Team 1 has to make %s points to win" % (30 - Bid))

def SetTrump(SetterName):
    print("%s, please select the trump from the below mentioned choices:" % SetterName)
    print("Press 1 for Heart")
    print("Press 2 for Diamonds")
    print("Press 3 for Spades")
    print("Press 4 for Clubs")
    TrumpSuite = 0
    while not TrumpSuite in range(1, len(COLORS) + 1):
        try:
            TrumpSuite = int(input("Enter the trump suite:"))
        except ValueError:
            """
            Error handling when input not an integer
            """
            print("That wasn't an integer :(")
    return COLORS[TrumpSuite - 1]

# def isTrumpOpen(TrumpIsOpenFlag):
def isTrumpValid(isTrumpOpen, TrumpSuite, card_color):
    if isTrumpOpen == True and card_color == TrumpSuite:
        return True
    else:
        return False

def CardValidityReset(hand_of_cards):
    for card in hand_of_cards:
        card.validity = 1
    return hand_of_cards

def updateCardValidity(card, TrickSuite, isTrumpOpen, TrumpSuite, sum_invalid_cards):
    if (card.color == TrickSuite) or (isTrumpValid(isTrumpOpen, TrumpSuite, card.color) == True):
        # Including all cards having color same as first player turn
        card.validity = 1
    else:
        card.validity = 0
        sum_invalid_cards = sum_invalid_cards + 1
    return card, sum_invalid_cards

def getValidCards(Player, cardsInATurn, isTrumpOpen, FirstPlayerofRound, TrumpSuite):
    sum_invalid_cards = 0
    if len(cardsInATurn) > 0:
        TrickSuite = cardsInATurn[FirstPlayerofRound].color
        for card in Player.hand:
            card, sum_invalid_cards = updateCardValidity(card, TrickSuite, isTrumpOpen, TrumpSuite, sum_invalid_cards)
        if sum_invalid_cards == len(Player.getHand()):
            # If player doesnt have either of these 2 suits, then all other cards are valid
            Player.hand = CardValidityReset(Player.hand)
    return Player.hand

def getValidIndex(ValidCards):
    valid_moves = []
    for i in range(0, len(ValidCards)):
        if ValidCards[i].validity == 1:
            valid_moves.append(i)
    return valid_moves