class Intent:

    def add_scores(self, wins, losses, draws):
        self.wins += wins
        self.losses += losses
        self.draws += draws

    def add_played_time(self, t):
        pass

    def commit(self):
        pass