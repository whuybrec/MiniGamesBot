class Player:
    def __init__(self, member):
        self.member = member
        self.name = self.member.name
        self.id = self.member.id
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.idle = False

    def is_idle(self):
        return self.idle

    def set_idle(self):
        self.idle = True
