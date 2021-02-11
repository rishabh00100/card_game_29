class Team():
    """
    Creating an object for each team having the following attributes:
        team_name:          Name of the team <str>
        game_points:        Game points of the team
        member1:            1st member of this team
        member2:            2nd member of this team
        member_list:        <list> of team members
        match_score:        match score of the teammembers combined
        req_match_score:    match score required by this team to win this match round
    """
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
        # Method to add match score incrementally during the match rounds of a game
        self.match_score += new_score

    def update_game_point(self, new_point):
        # Method to add game points incrementally during the game
        self.game_points += new_point

    def update_req_match_score(self, req_score):
        # Method to set req_match_score after betting round
        self.req_match_score = req_score

    def reset_match_data(self):
        # Method to reset the match_score and req_match_score at the start of every match round
        self.match_score = 0
        self.req_match_score = 0

    def printMatchScore(self):
        print(">>> Match score of {team_name}: {score}".format(team_name = self.team_name, score = self.match_score))

    def printGamePoint(self):
        print(">>> Game points of {team_name}: {score}".format(team_name = self.team_name, score = self.game_points))