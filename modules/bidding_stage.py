class BiddingStage:
    """
    Class for biding rounds
    """
    def __init__(self, player_list, display_obj, round_number):
        print("***************STARTING BETTING ROUND***************")
        self.round_number = round_number
        self.PassCounter = 0    # Number of players that have passed their bid
        self.CurrentBidder, self.OppBidder = 0, 1
        self.HigherBid = 0
        self.player_list = player_list
        self.HigherBidder = self.player_list[self.CurrentBidder]
        self.Bidder1High = True
        self.MINIMUM_BET = 17
        self.MAXIMUM_BET = 29
        self.display_obj = display_obj
        self.startBiddingRound()

    def setBid(self, Bid, BidderName):
        if Bid == 0:
            return True
        else:
            self.HigherBid = Bid
            self.HigherBidder = BidderName
            return False

    def increase_pass_counter(self):
        self.PassCounter += 1

    def isAllPlayerPass(self, verbose=False):
        if self.PassCounter == len(self.player_list):
            if verbose:
                print("**** ALL PLAYERS HAVE PASSED THE BIDS")
            return True
        else:
            return False

    def AllPlayerPassCondition(self):
        if self.isAllPlayerPass():
            is_pass_flag = self.setBid(self.MINIMUM_BET+1, self.player_list[0])   # Default Player1 becomes the highest bidder at 18 points
            self.player_list[0].bid = self.HigherBid

    def rotateBidder(self):
        if self.CurrentBidder < self.OppBidder and self.HigherBid > 0:
            self.CurrentBidder = self.OppBidder + 1
        elif self.CurrentBidder < self.OppBidder and self.HigherBid == 0:
            self.CurrentBidder = self.CurrentBidder + 1
            self.OppBidder = self.OppBidder + 1
        elif self.CurrentBidder > self.OppBidder:
            self.CurrentBidder = self.CurrentBidder + 1

    def BidExitCondition(self, verbose=False):
        if self.PassCounter >= 3 and self.HigherBid > 0:
            if verbose:
                print("**** BID EXIT CONDITION HIT")
            return True
        else:
            return False

    def update_GC_state(self, state):
        stage_name = "Bidding Phase - {}".format(self.round_number)
        show_img = True
        allowed_inputs = None
        if state == 1:
            if self.current_bid == 0:
                heading = "{} has decided to pass the bidding".format(self.player_list[self.CurrentBidder])
            else:
                heading = "{} has set the bid to {}".format(self.player_list[self.CurrentBidder], self.current_bid)
            sub_heading = None
            action_line = "Press anything to continue..."
        elif state == 2:
            heading = "{} won the betting round and will play to make {} points".format(self.HigherBidder.team, self.HigherBid)
            sub_heading = "{} has to make {} points to stop {} from winning".format(self.losing_team, (30 - self.HigherBid), self.HigherBidder.team)
            action_line = "{} will set the trump. Press anything to continue...".format(self.HigherBidder)

        player_input = self.display_obj.update_game_console(stage_name=stage_name, heading=heading, sub_heading=sub_heading, 
                                                            action_line=action_line, allowed_inputs=allowed_inputs, show_img=show_img)


    def biddingModule(self, newBid, verbose=True):
        self.exit_flag = True
        while self.exit_flag:
            if verbose:
                print("-"*60)
                print("CurrentBidder: {} | OppBidder: {} | newBid: {}".format(self.CurrentBidder, self.OppBidder, newBid))
                print("HigherBid: {} | HigherBidder: {} | PassCounter: {}".format(self.HigherBid, self.HigherBidder, self.PassCounter))
                print("-"*60)
            self.current_bid = self.player_list[self.CurrentBidder].getBet(newBid, self.MAXIMUM_BET, self.display_obj, self.round_number)
            is_pass_flag = self.setBid(self.current_bid, self.player_list[self.CurrentBidder])
            self.display_obj.update_player_console()
            self.update_GC_state(state=1)
            if is_pass_flag:
                self.increase_pass_counter()
                self.AllPlayerPassCondition()
                if self.BidExitCondition():
                    self.exit_flag = False
                    break
                self.rotateBidder()
                self.biddingModule(newBid)
            else:
                if self.HigherBid == self.MAXIMUM_BET:
                    self.exit_flag = False
                    break
                self.CurrentBidder, self.OppBidder = self.OppBidder, self.CurrentBidder
                self.biddingModule(self.HigherBid)

    def startBiddingRound(self):
        self.biddingModule(self.MINIMUM_BET, True)

    def DeclareBidWinner(self):
        # if self.HigherBidder in team1.member_list:
        #     print("Team 1 won the betting round and will play to make %s points" % self.HigherBid)
        #     print("%s will set the trump" % self.HigherBidder)
        #     print("Team 2 has to make %s points to win" % (30 - self.HigherBid))
        # else:
        #     print("Team 2 won the betting round and will play to make %s points" % self.HigherBid)
        #     print("%s will set the trump" % self.HigherBidder)
        #     print("Team 1 has to make %s points to win" % (30 - self.HigherBid))
        # return self.HigherBidder
        print("\n*********************************************************************")
        print("{} won the betting round and will play to make {} points".format(self.HigherBidder.team, self.HigherBid))
        print("{} will set the trump".format(self.HigherBidder))
        print("Other team has to make {} points to stop {} from winning".format((30 - self.HigherBid), self.HigherBidder.team))
        print("*********************************************************************\n")
        self.winning_team = self.HigherBidder.team
        self.winning_team.update_req_match_score(self.HigherBid)
        self.losing_team = None
        for player in self.player_list:
            if player.team != self.winning_team:
                self.losing_team = player.team
                break
        self.losing_team.update_req_match_score(30 - self.HigherBid)
        self.update_GC_state(state=2)
        return self.HigherBidder, self.HigherBid
