import time

from Database.database import DataBase
from Database.intent import Intent
from Other.variables import Variables


class Intent_master:
    def __init__(self, server_id, user_id, game_name):
        self.server_id = server_id
        self.user_id = user_id
        self.game_name = game_name
        self.min_time_played = 0
        self.max_time_played = 0
        self.t_start = time.time()
        self.first_time_played = time.time()
        self.last_time_played = time.time()
        self.total_time_played = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0

        master = DataBase.run("""SELECT * FROM master WHERE server_id = {0} AND user_id = {1} AND game_name = '{2}'"""
                              .format(server_id, user_id, game_name))
        if len(master) != 0:
            attributes = list(master[0])
            self.wins = attributes[3]
            self.losses = attributes[4]
            self.draws = attributes[5]
            self.total_time_played = attributes[6]
            self.min_time_played = attributes[7]
            self.max_time_played = attributes[8]
            self.first_time_played = attributes[9]
        else:
            DataBase.insert_master_row((self.server_id, self.user_id, self.game_name, self.wins, self.losses, self.draws, self.total_time_played, self.min_time_played, self.max_time_played, self.first_time_played, self.last_time_played))

    def add_played_time(self, t):
        if t < 0:
            return
        self.total_time_played += t
        if t < self.min_time_played:
            self.min_time_played = t
        elif t > self.max_time_played:
            self.max_time_played = t

    def commit(self, timeout=True):
        t_end = time.time()
        diff = t_end - self.t_start
        if timeout:
            diff -= Variables.TIMEOUT
        self.add_played_time(diff)
        DataBase.run("""UPDATE master SET wins={0}, losses={1}, draws={2}, total_time_played={3}, 
               min_time_played={4}, max_time_played={5}, first_time_played={6}, last_time_played={7} 
               WHERE server_id = {8} AND user_id = {9} AND game_name = '{10}'"""
                     .format(self.wins, self.losses, self.draws, self.total_time_played, self.min_time_played,
                             self.max_time_played, self.first_time_played, self.last_time_played, self.server_id,
                             self.user_id, self.game_name))

    def add_scores(self, wins, losses, draws):
        self.wins += wins
        self.losses += losses
        self.draws += draws
