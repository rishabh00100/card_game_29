import random

COLORS = ['Heart', 'Diamonds', 'Spades', 'Clubs']
VALUES = ['Ace', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
MINIMUM_BET = 17
MAXIMUM_BET = 29
VALIDITY = 1

class Card:
    """Creating an object for each card
    has following attributes:
    Value = Face Value of the card
    Color = Corresponding to one of the 4 suits in a card deck
    Score = Score of the card in this game
    win_priority = priority of the card in deciding hand winner
    Validity = 1 if card is valid to play in that turn else 0
    """
    def __init__(self, value, color, validity):
        self.value = value
        self.color = color
        self.validity = validity
        self.setCardScore()

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

    def setCardScore(self):
        """
        Returns a string containing the card's name in common terms.
        """
        if self.value == 'Jack':
            self.score = 3
            self.win_priority = 1
        elif self.value == '9':
            self.score = 2
            self.win_priority = 2
        elif self.value == 'Ace':
            self.score = 1
            self.win_priority = 3
        elif self.value == '10':
            self.score = 1
            self.win_priority = 4
        elif self.value == 'King':
            self.score = 0
            self.win_priority = 5
        elif self.value == 'Queen':
            self.score = 0
            self.win_priority = 6
        elif self.value == '8':
            self.score = 0
            self.win_priority = 7
        elif self.value == '7':
            self.score = 0
            self.win_priority = 8

class DeckOfCards:

    def __init__(self):
        # Initializes a dexk of card for 29 card game
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
    """Creating an object for each player
    has following attributes:
    name = Name of the player
    hand = current set of cards that the player is holding
    score = score of the hands owned by this player
    bid = total points that this player has bid for
    bidpass = flag representing if the player has passed in the current bidding round
    """
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

    def calcScoreOfHand(self):
        score = 0
        for each_card in self.hand:
            score += each_card.score
        return score

    def printScoreOfHand(self):
        score = self.calcScoreOfHand()
        print("{player_name}, you are having cards worth {total_score} points".format(player_name=self.name, total_score=score))

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
                print("{player_name}, this is your hand for reference".format(player_name=self.name))
                self.showHand()
                self.printScoreOfHand()
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

class BiddingRound:
    """
    Class for biding rounds
    """
    def __init__(self, PlayerSet):
        print("***************STARTING BETTING ROUND***************")
        self.PassCounter = 0
        self.FirstBidder, self.SecondBidder = 0, 1
        self.HigherBid = 0
        self.HigherBidder = PlayerSet[0].name
        self.Bidder1High = True
        self.PlayerSet = PlayerSet

    def startBiddingRound(self):
        self.FirstBidder, self.SecondBidder = self.biddingModule(self.FirstBidder, self.SecondBidder, MINIMUM_BET)

    def biddingModule(self, FirstBidder, SecondBidder, newBid):
        while self.Bidder1High == True:
            newerBid, newerBidder = self.setBid(self.PlayerSet[FirstBidder].getBet(newBid), self.PlayerSet[FirstBidder].name)
            if self.PlayerSet[FirstBidder].isBidPass(newerBid):
                self.PassCounter = self.PassCounter + 1
                self.PlayerSet[FirstBidder].bidpass = True
                self.PlayerSet = self.AllPlayerPassCondition()
                FirstBidder, SecondBidder = self.incrementBidder(FirstBidder, SecondBidder, self.HigherBid)
                if self.BidExitCondition():
                    self.Bidder1High = False
                    break
                FirstBidder, SecondBidder = self.biddingModule(FirstBidder, SecondBidder, newBid)
            else:
                self.HigherBid, self.HigherBidder = self.setBid(newerBid, newerBidder)
                self.PlayerSet[FirstBidder].bid = self.HigherBid
                if self.HigherBid == MAXIMUM_BET:
                    self.Bidder1High = False
                    break
                FirstBidder, SecondBidder = self.biddingModule(SecondBidder, FirstBidder, newerBid)
        return FirstBidder, SecondBidder

    def setBid(self, Bid, BidderName):
        self.HigherBid = Bid
        self.HigherBidder = BidderName
        return self.HigherBid, self.HigherBidder

    def isAllPlayerPass(self):
        if self.PassCounter == len(self.PlayerSet):
            return True
        else:
            return False

    def AllPlayerPassCondition(self):
        if self.isAllPlayerPass():
            self.HigherBid, self.HigherBidder = self.setBid(MINIMUM_BET, self.PlayerSet[0].name)
            self.PlayerSet[0].bid = self.HigherBid
        else:
            self.HigherBid, self.HigherBidder = self.setBid(self.HigherBid, self.HigherBidder)
        return self.PlayerSet

    def incrementBidder(self, FirstBidder, SecondBidder, HigherBid):
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

    def BidExitCondition(self):
        if self.PassCounter >= 3 and self.HigherBid > 0:
            return True
        else:
            return False

    def DeclareBidWinner(self, Team1):
        if self.HigherBidder in Team1:
            print("Team 1 won the betting round and will play to make %s points" % self.HigherBid)
            print("%s will set the trump" % self.HigherBidder)
            print("Team 2 has to make %s points to win" % (30 - self.HigherBid))
        else:
            print("Team 2 won the betting round and will play to make %s points" % self.HigherBid)
            print("%s will set the trump" % self.HigherBidder)
            print("Team 1 has to make %s points to win" % (30 - self.HigherBid))
        return self.HigherBidder



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

class PlayRound:
    def __init__(self):
        print("***************LETS START THE GAME***************")

    def SetTrump(self, SetterName):
        print("SETTING TRUMP")
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

def filterPassCards(listOfCards):
    # Remove all the cards that are played as pass
    # This is because pass cards cannot win the hand
    return

def filterForTrumpCards(listOfCards):
    # Return all the trump cards in this hand
    # If no trump card is played, return all cards
    return

def selectWinningCard(listOfCards):
    listOfCards = filterPassCards(listOfCards)
    listOfCards = filterForTrumpCards(listOfCards)
    listOfPriorities = [i.win_priority for i in listOfCards]
    winningPriority = min(listOfPriorities)
    for each_card in listOfCards:
        if each_card.win_priority == winningPriority:
            return each_card

def CalcHandWinner(cardsInATurn):
    listOfCards = cardsInATurn.values()
    winningCard = selectWinningCard(listOfCards)
    winningPlayer = cardsInATurn.get(winningCard)