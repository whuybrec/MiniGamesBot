class Player:
    def __init__(self, member):
        self.member = member
        self.name = self.member.name
        self.id = self.member.id

        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.unfinished = 0
        self.total_games = 0

    def get_total_played_games(self):
        return self.total_games

    def win(self):
        self.wins += 1

    def lose(self):
        self.losses += 1

    def draw(self):
        self.draws += 1

    def did_not_finish(self):
        self.unfinished += 1

    def played(self):
        self.total_games += 1

    def get_stats(self):
        return {
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "unfinished": self.unfinished,
            "total_games": self.total_games
        }
