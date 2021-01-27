# from modules.utils import *
from modules.team import Team
from modules.player import Player
from modules.match_round import MatchRound

class Game_of_29(MatchRound, Team, Player):
    def __init__(self, team1, team2, player1_name, player2_name, player3_name, player4_name):
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        self.player3 = Player(player3_name)
        self.player4 = Player(player4_name)
        self.player_list = [self.player1, self.player2, self.player3, self.player4]

        self.team1 = Team(team1, self.player1, self.player3)
        self.team2 = Team(team2, self.player2, self.player4)
        self.team_list = [self.team1, self.team2]

    def start_match(self):
        while True:
            if abs(self.team1.game_points) >= 5 or abs(self.team2.game_points) >= 5:
                break
            MatchRound(self.player_list, self.team_list)