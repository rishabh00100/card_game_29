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

    def showHandToPlay(self, round_number):
        size = len(self.hand)
        valid_index = []
        for i in range(0, size):
            if self.hand[i].validity == 1:
                print("Press {i} for {card}".format(i = i, card = self.hand[i]))
                valid_index.append(i)
        player_input_card = int(self.update_GC_state(state=4, valid_index=valid_index, r_index=round_number))
        return player_input_card

    def update_GC_state(self, state, **kwargs):
        action_line = None
        heading = None
        sub_heading = None
        allowed_inputs = None
        show_img = True
        if state == 1:
            stage_name = "Bidding Phase - {}".format(kwargs["r_index"])
            heading = "{}, do you want to bid for {} points or pass the bid?".format(self.name, kwargs["opp_bet"] + 1)
            action_line = "{}, press 1 to bid or 0 to pass".format(self.name)
            allowed_inputs = [0,1]
        elif state == 2:
            stage_name = "Bidding Phase - {}".format(kwargs["r_index"])
            sub_heading = "That wasn't an integer :("
            action_line = "Press anything to continue..."
        elif state == 3:
            stage_name = "Bidding Phase - {}".format(kwargs["r_index"])
            sub_heading = "Invalid bet, please try again."
            action_line = "Press anything to continue..."
        elif state == 4:
            stage_name = "Play Phase - {}".format(kwargs["r_index"])
            action_line = "{}, select your card to play".format(self.name)
            allowed_inputs = kwargs["valid_index"]
        player_input = self.display_obj.update_game_console(stage_name=stage_name, heading=heading, sub_heading=sub_heading, 
                                                            action_line=action_line, allowed_inputs=allowed_inputs, show_img=show_img)
        return player_input

    def getBet(self, Opponent_Bet, MAXIMUM_BET, display_obj, round_number):
        self.display_obj = display_obj
        playerBet = -1
        while not playerBet in [range(0, MAXIMUM_BET+1)]:
            try:
                playerBet = int(self.update_GC_state(state=1, opp_bet=Opponent_Bet, r_index=round_number))

                # Codes for game display on terminal
                # print("{player_name}, this is your hand for reference".format(player_name=self.name))
                # self.showHand()
                # self.printScoreOfHand()
                # playerBet = int(input("%s Please input your bet between %s and %s or input 0 to pass/end betting:" %(self.name, Opponent_Bet + 1, MAXIMUM_BET)))
            except ValueError:
                # Error handling when input not an integer
                _ = self.update_GC_state(state=2, opp_bet=Opponent_Bet, r_index=round_number)
                print("That wasn't an integer :(")
                continue

            if playerBet == 0:
                # Player has passed the bidding
                self.bid = 0
                self.bidpass = True
                return playerBet
            # elif playerBet <= Opponent_Bet:
            #     _ = self.update_GC_state(state=3, opp_bet=Opponent_Bet)
            #     print('Invalid bet, please try again.')
            else:
                self.bid = Opponent_Bet+1
                return self.bid

    def isBidPass(self, playerBet):
        if playerBet == 0:
            return True
        else:
            return False