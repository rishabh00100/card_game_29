from modules.player import Player

class Team(Player):
    def __init__(self, team_name, player1_obj, player2_obj):
        self.team_name = team_name
        self.reset_match_data()
        self.game_points = 0
        self.member1 = player1_obj
        self.member2 = player2_obj
        self.member1.set_team(self)
        self.member2.set_team(self)
        self.member_list = [self.member1, self.member2]

    def __str__(self):
        return self.team_name

    def update_score(self, new_score):
        self.match_score += new_score

    def update_game_point(self, new_point):
        self.game_points += new_point

    def reset_match_data(self):
        self.match_score = 0

    def printMatchScore(self):
        print(">>> Match score of {team_name}: {score}".format(team_name = self.team_name, score = self.match_score))

    def printGamePoint(self):
        print(">>> Game points of {team_name}: {score}".format(team_name = self.team_name, score = self.game_points))