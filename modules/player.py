class Player(object):
    """Creating an object for each player
    has following attributes:
    name = Name of the player
    hand = current set of cards that the player is holding
    score = score of the hands owned by this player
    bid = total points that this player has bid for
    bidpass = flag representing if the player has passed in the current bidding round
    """
    def __init__(self, name):
        self.name = name
        self.team = None
        self.reset_match_data()

    def __str__(self):
        return self.name

    def set_team(self, team):
        self.team = team

    def reset_match_data(self):
        self.hand = []
        self.bid = 0
        self.score = 0
        self.bidpass = False
        self.did_select_trump = False

    def getScore(self):
        return self.score

    def getHand(self):
        return self.hand

    def calcScoreOfHand(self):
        score = 0
        for each_card in self.hand:
            score += each_card.score
        return score

    def printScoreOfHand(self):
        score = self.calcScoreOfHand()
        print("{player_name}, you are having cards worth {total_score} points".format(player_name=self.name, total_score=score))

    def printScore(self):
        print(">>> Score of {player_name}: {score}".format(player_name = self.name, score = self.score))

    def update_score(self, new_score):
        self.score += new_score

    def reset_score(self):
        self.score = 0

    def showHand(self):
        size = len(self.hand)
        for i in range(0, size):
            print(self.hand[i])

    def showHandToPlay(self):
        size = len(self.hand)
        for i in range(0, size):
            if self.hand[i].validity == 1:
                print("Press {i} for {card}".format(i = i, card = self.hand[i]))

    def getBet(self, Opponent_Bet, MAXIMUM_BET):
        playerBet = -1
        while not playerBet in [range(0, MAXIMUM_BET+1)]:
            try:
                print("{player_name}, this is your hand for reference".format(player_name=self.name))
                self.showHand()
                self.printScoreOfHand()
                playerBet = int(input("%s Please input your bet between %s and %s or input 0 to pass/end betting:" %(self.name, Opponent_Bet + 1, MAXIMUM_BET)))
            except ValueError:
                # Error handling when input not an integer
                print("That wasn't an integer :(")
                continue

            if playerBet == 0:
                # Player has passed the bidding
                self.bid = playerBet
                self.bidpass = True
                return playerBet
            elif playerBet <= Opponent_Bet:
                print('Invalid bet, please try again.')
            else:
                self.bid = playerBet
                return playerBet

    def isBidPass(self, playerBet):
        if playerBet == 0:
            return True
        else:
            return False