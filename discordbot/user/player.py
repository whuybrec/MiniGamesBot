class Player:
    def __init__(self, member):
        self.member = member
        self.name = self.member.name
        self.id = self.member.id
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.unfinished = 0

    def get_total_played_games(self):
        return self.wins + self.losses + self.draws
