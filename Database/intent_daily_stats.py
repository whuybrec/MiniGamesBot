import time

from Database.database import DataBase
from Database.intent import Intent
from Other.variables import Variables


class Intent_daily_stats:
    def __init__(self, server_id, game_name):
        self.date = time.strftime("%Y-%m-%d")
        self.t_start = time.time()
        self.server_id = server_id
        self.game_name = game_name
        self.total_time_played = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0

        daily_stats = DataBase.run("""SELECT * FROM daily_stats WHERE date_ = '{0}' AND server_id = {1} AND game_name = '{2}'"""
                              .format(self.date, server_id, game_name))
        if len(daily_stats) != 0:
            attributes = list(daily_stats[0])
            self.wins = attributes[3]
            self.losses = attributes[4]
            self.draws = attributes[5]
            self.total_time_played = attributes[6]
        else:
            DataBase.insert_daily_stats_row((
                                       self.date, self.server_id, self.game_name, self.wins, self.losses, self.draws,
                                       self.total_time_played))

    def add_played_time(self, t):
        if t < 0:
            return
        self.total_time_played += t

    def commit(self, timeout=True):
        t_end = time.time()
        diff = t_end - self.t_start
        if timeout:
            diff -= Variables.TIMEOUT
        self.add_played_time(diff)
        DataBase.run(
            """UPDATE daily_stats SET wins={0}, losses={1}, draws={2}, total_time_played={3} WHERE date_ = '{4}' AND server_id = {5} AND game_name = '{6}'"""
            .format(self.wins, self.losses, self.draws, self.total_time_played, self.date,
                    self.server_id, self.game_name))

    def add_scores(self, wins, losses, draws):
        self.wins += wins
        self.losses += losses
        self.draws += draws