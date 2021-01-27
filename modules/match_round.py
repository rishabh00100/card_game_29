from modules.bidding_stage import BiddingStage
from modules.play_stage import PlayStage
from modules.deck_of_cards import DeckOfCards

class MatchRound(DeckOfCards):
    def __init__(self, player_list, team_list):
        self.player_list = player_list
        self.team_list = team_list
        self.prepare_deck_of_cards()
        self.reset_team_match_scores()
        self.deal_starting_cards()
        self.start_bidding_stage()
        self.start_play_stage()

    def reset_team_match_scores(self):
        for team in self.team_list:
            team.reset_match_data()
        for player in self.player_list:
            player.reset_score()

    def prepare_deck_of_cards(self):
        self.deckofCards = DeckOfCards()
        for i in range(0, 10):
            self.deckofCards.shuffleDeck()

    def deal_starting_cards(self):
        print("DISTRIBUTING 4 CARDS PER PLAYER")
        self.deckofCards.dealCards(self.player_list)

    def start_bidding_stage(self):
        BidRound = BiddingStage(self.player_list)
        self.HigherBidder, self.HigherBid = BidRound.DeclareBidWinner()

    def start_play_stage(self):
        FirstRound = PlayStage(self.HigherBidder, self.HigherBid, self.deckofCards, self.player_list, self.team_list)
        print("DEALING REMAINING CARDS")
        self.deckofCards.dealCards(self.player_list)
        print("LETS START THE GAME")
        for i in range(8):
            FirstRound.lets_play_this_round(i+1)

        for team in self.team_list:
            if self.HigherBidder.team == team:
                if team.match_score >= self.HigherBid:
                    # This team set the bid and won the match
                    print("{} set the bid at {} and made {} points and won!!".format(team, self.HigherBid, team.match_score))
                    team.update_game_point(1)
                else:
                    # This team set the bid and lost the match
                    print("{} set the bid at {} and made {} points and lost :(".format(team, self.HigherBid, team.match_score))
                    team.update_game_point(-1)
            team.printMatchScore()
            team.printGamePoint()