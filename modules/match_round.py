from modules.bidding_stage import BiddingStage
from modules.play_stage import PlayStage
from modules.deck_of_cards import DeckOfCards
from modules.utils import *
import cv2
import time

class MatchRound(DeckOfCards):
    def __init__(self, player_list, team_list, round_number):
        self.round_number = round_number
        self.player_list = player_list
        self.team_list = team_list
        self.prepare_deck_of_cards()
        self.reset_team_match_scores()
        # Display should start from here
        self.displ_obj = cv2_display(self.player_list, self.round_number)
        _ = self.update_GC_state(state=4)
        self.deal_starting_cards()
        self.start_bidding_stage()
        self.start_play_stage()

    def reset_team_match_scores(self):
        for team in self.team_list:
            team.reset_match_data()
        for player in self.player_list:
            player.reset_match_data()

    def prepare_deck_of_cards(self):
        self.deckofCards = DeckOfCards()
        for i in range(0, 10):
            self.deckofCards.shuffleDeck()

    def deal_starting_cards(self):
        print("DISTRIBUTING 4 CARDS PER PLAYER")
        self.deckofCards.dealCards(self.player_list)
        self.displ_obj.display_game_state(self.player_list)

    def start_bidding_stage(self):
        BidRound = BiddingStage(self.player_list, self.displ_obj, self.round_number)
        self.HigherBidder, self.HigherBid = BidRound.DeclareBidWinner()

    def update_GC_state(self, state, **kwargs):
        stage_name = "Play Phase - {}".format(self.round_number)
        allowed_inputs = None
        show_img = True
        if state == 1:
            heading = "Distributing 4 more cards per player to start playing"
            sub_heading = None
            action_line = "Let's start the game. Press anything to continue..."
        if state == 2:
            heading = "{} set the bid at {} and made {} points and won!!".format(kwargs["a"], kwargs["b"], kwargs["c"])
            sub_heading = None
            action_line = "Press anything to continue..."
        if state == 3:
            heading = "{} set the bid at {} and made {} points and lost :(".format(kwargs["a"], kwargs["b"], kwargs["c"])
            sub_heading = None
            action_line = "Press anything to continue..."
        if state == 4:
            stage_name = "Starting Phase - {}".format(self.round_number)
            heading = "Distributing 4 cards per player to start bidding"
            sub_heading = None
            action_line = "Press anything to continue..."

        player_input = self.displ_obj.update_game_console(stage_name=stage_name, heading=heading, sub_heading=sub_heading, 
                                                            action_line=action_line, allowed_inputs=allowed_inputs, show_img=show_img)
        if show_img:
            return player_input
        else:
            return None

    def start_play_stage(self):
        FirstRound = PlayStage(self.HigherBidder, self.HigherBid, self.deckofCards, self.player_list, self.team_list, self.displ_obj, self.round_number)
        print("DEALING REMAINING CARDS")
        self.deckofCards.dealCards(self.player_list)
        self.displ_obj.display_game_state(self.player_list)
        # player_input = self.displ_obj.update_game_console(flag=2)
        _ = self.update_GC_state(state=1)
        time.sleep(0.2)
        print("LETS START THE GAME")
        for i in range(8):
            FirstRound.lets_play_this_round(i+1)

        for team in self.team_list:
            if self.HigherBidder.team == team:
                self.displ_obj.update_player_console()
                if team.match_score >= self.HigherBid:
                    # This team set the bid and won the match
                    print("{} set the bid at {} and made {} points and won!!".format(team, self.HigherBid, team.match_score))
                    team.update_game_point(1)
                    _ = self.update_GC_state(state=2, a=team, b=self.HigherBid, c=team.match_score)
                else:
                    # This team set the bid and lost the match
                    print("{} set the bid at {} and made {} points and lost :(".format(team, self.HigherBid, team.match_score))
                    team.update_game_point(-1)
                    _ = self.update_GC_state(state=3, a=team, b=self.HigherBid, c=team.match_score)
            team.printMatchScore()
            team.printGamePoint()

        # _ = self.displ_obj.update_game_console(flag=3, )








