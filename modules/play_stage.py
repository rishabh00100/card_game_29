import time

class PlayStage:
    def __init__(self, SetterName, SetterBid, deckofCards, player_list, team_list):
        print("***************LETS START THE GAME***************")
        self.deckofCards = deckofCards
        self.TrumpSuite = self.SetTrump(SetterName)
        self.isTrumpOpen = False
        self.player_list = player_list
        self.team_list = team_list
        self.FirstPlayerofRound = SetterName
        self.BidSetter = SetterName
        self.BidForRound = SetterBid

    def SetTrump(self, SetterName):
        print("SETTING TRUMP")
        print("%s, please select the trump from the below mentioned choices:" % SetterName)
        print("Press 1 for Heart")
        print("Press 2 for Diamonds")
        print("Press 3 for Spades")
        print("Press 4 for Clubs")
        TrumpSuite = 0
        while not TrumpSuite in range(1, len(self.deckofCards.COLORS) + 1):
            try:
                TrumpSuite = int(input("Enter the trump suite:"))
            except ValueError:
                # Error handling when input not an integer
                print("That wasn't an integer :(")
        return self.deckofCards.COLORS[TrumpSuite - 1]

    def CardValidityReset(self, hand_of_cards):
        for card in hand_of_cards:
            card.validity = 1
        return hand_of_cards

    def isTrumpValid(self, card_color):
        if self.isTrumpOpen == True and card_color == self.TrumpSuite:
            return True
        else:
            return False

    def updateCardValidity2(self, card, TrickSuite, sum_invalid_cards):
        if (card.color == TrickSuite):
            # Including all cards having color same as first player turn
            card.validity = 1
        else:
            card.validity = 0
            sum_invalid_cards = sum_invalid_cards + 1
        return sum_invalid_cards

    def updateCardValidity1(self, card, TrickSuite, sum_invalid_cards):
        if card.color == self.TrumpSuite:
            # Including all cards having color same as first player turn
            card.validity = 1
        else:
            card.validity = 0
            sum_invalid_cards = sum_invalid_cards + 1
        return sum_invalid_cards

    def getValidCards(self, Player, cardsInATurn, FirstPlayerofRound, isTrumpOpenFlag=False):
        sum_invalid_cards = 0
        count_trumps = 0
        valid_moves = []
        if len(cardsInATurn) > 0:
            TrickSuite = cardsInATurn[FirstPlayerofRound].color
            if isTrumpOpenFlag:
                print(">>> Received isTrumpOpenFlag")
                for card in Player.hand:
                    sum_invalid_cards = self.updateCardValidity1(card, TrickSuite, sum_invalid_cards)
                    if sum_invalid_cards == len(Player.getHand()):
                        print("{} does not have any trump cards".format(Player))
                        Player.hand = self.CardValidityReset(Player.hand)
                        sum_invalid_cards = 0
            else:
                for card in Player.hand:
                    sum_invalid_cards = self.updateCardValidity2(card, TrickSuite, sum_invalid_cards)
                if sum_invalid_cards == len(Player.getHand()):
                    # If player doesnt have either of these 2 suits, then all other cards are valid
                    Player.hand = self.CardValidityReset(Player.hand)
                    if not self.isTrumpOpen:
                        valid_moves.append(1111)
                        print("{} does not have any valid card. You can open trump suite".format(Player))
                # else:
                #     # Check and add Trump suite cards
                #     for card in Player.hand:
                #         if self.isTrumpValid(card.color) == True:
                #             card.validity = 1
                #             sum_invalid_cards -= 1

            # if sum_invalid_cards == len(Player.getHand()):
            #     # If player doesnt have either of these 2 suits, then all other cards are valid
            #     Player.hand = self.CardValidityReset(Player.hand)
            #     if not self.isTrumpOpen:
            #         valid_moves.append(1111)
        else:
            Player.hand = self.CardValidityReset(Player.hand)
        
        for i in range(0, len(Player.hand)):
            if Player.hand[i].validity == 1:
                valid_moves.append(i)

        return Player.hand, valid_moves

    def CalcHandWinner(self, cardsInATurn, FirstPlayerofRound, round_number):
        TrickSuite = cardsInATurn[FirstPlayerofRound].color
        listOfCards = list(cardsInATurn.values())
        winningCard, winScore = self.selectWinningCard(listOfCards, TrickSuite)
        winningPlayer = [k for k, v in cardsInATurn.items() if v==winningCard][0]
        print("List of cards:")
        for i in listOfCards:
            print("\t", i)
        print(">>> winning card:", winningCard)
        print(">>> winning player:", winningPlayer)
        print(">>> winning score:", winScore)
        # Update scores for winners

        if round_number == 8:
            # Winner of last round gets 1 extra point
            winScore += 1

        winningPlayer.update_score(winScore)
        winningPlayer.team.update_score(winScore)
        self.FirstPlayerofRound = winningPlayer

    def filterPassCards(self, listOfCards, TrickSuite):
        # Remove all the cards that are played as pass
        # This is because pass cards cannot win the hand
        new_listOfCards = []
        for each_card in listOfCards:
            if each_card.color != TrickSuite and (self.isTrumpValid(each_card.color) == False):
                pass
            else:
                new_listOfCards.append(each_card)
        return new_listOfCards

    def filterForTrumpCards(self, listOfCards):
        # Return all the trump cards in this hand
        # If no trump card is played, return all cards
        new_listOfCards = []
        for each_card in listOfCards:
            if self.isTrumpValid(each_card.color) == True:
                new_listOfCards.append(each_card)
        if len(new_listOfCards) > 0:
            return new_listOfCards
        else:
            return listOfCards

    def selectWinningCard(self, listOfCards, TrickSuite):
        listOfScores = [i.score for i in listOfCards]
        listOfCards = self.filterPassCards(listOfCards, TrickSuite)
        listOfCards = self.filterForTrumpCards(listOfCards)
        listOfPriorities = [i.win_priority for i in listOfCards]
        winningPriority = min(listOfPriorities)
        for each_card in listOfCards:
            if each_card.win_priority == winningPriority:
                return each_card, sum(listOfScores)

    def set_player_list(self):
        start_index = self.player_list.index(self.FirstPlayerofRound)
        new_player_list = self.player_list[start_index:]
        delta = len(self.player_list) - len(new_player_list)
        if delta > 0:
            new_player_list.extend(self.player_list[:delta])
        return new_player_list

    def display_cards(self, cardsInATurn):
        print("\n----------------------------------------------")
        for player, card in cardsInATurn.items():
            print("\t{}, {}".format(player, card))
        print("----------------------------------------------\n")

    def lets_play_this_round(self, round_number, verbose=True):
        print("\n************** START ROUND {} ******************".format(round_number))
        
        cardsInATurn = {}
        new_player_list = self.set_player_list()

        for player in new_player_list:
            if verbose:
                print("\n----------------------------------------------")
                print("\tisTrumpOpen", self.isTrumpOpen)
                print("\tTrumpSuite", self.TrumpSuite)
                print("----------------------------------------------\n")
            CardPlayed = 999
            print("{PlayerName}, your turn to play".format(PlayerName = player))
            ValidCards, valid_moves = self.getValidCards(player, cardsInATurn, self.FirstPlayerofRound)
            player.showHandToPlay()
            print(valid_moves)
            if len(valid_moves) == 1:
                CardPlayed = valid_moves[0]
                print("Selecting default option")
                time.sleep(2)
            else:
                while CardPlayed not in valid_moves:
                    try:
                        CardPlayed = int(input("Play:"))
                        if CardPlayed == 1111:
                            print("Open Trump selected by {}: {}".format(player, self.TrumpSuite))
                            valid_moves.remove(CardPlayed)
                            self.isTrumpOpen = True
                            ValidCards, valid_moves = self.getValidCards(player, cardsInATurn, self.FirstPlayerofRound, True)
                            player.showHandToPlay()
                    except ValueError:
                        print("Please provide integer input")
            cardsInATurn[player] = player.hand[CardPlayed]
            player.hand.pop(CardPlayed)
            self.display_cards(cardsInATurn)
        
        self.CalcHandWinner(cardsInATurn, self.FirstPlayerofRound, round_number)

        for player in self.player_list:
            player.printScore()

        for team in self.team_list:
            team.printMatchScore()























