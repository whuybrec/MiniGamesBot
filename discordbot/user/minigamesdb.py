from datetime import date
from generic.database import Database

FILE = "bin/minigames.db"


class MinigamesDB:
    database: Database

    @classmethod
    def on_startup(cls):
        cls.database = Database(FILE)
        cls.database.create_table(
            "players",
            [
                "player_id integer",
                "minigame text",
                "date text",
                "total_games integer",
                "wins integer",
                "losses integer",
                "draws integer",
                "time_played integer"
            ],
            [
                "player_id",
                "minigame",
                "date"
            ]
        )
        cls.database.create_table(
            "minigames",
            [
                "server_id integer",
                "minigame text",
                "date text",
                "total_games",
                "wins integer",
                "losses integer",
                "draws integer",
                "time_played integer"
            ],
            [
                "server_id",
                "minigame",
                "date"
            ]
        )

    @classmethod
    def add_to_players_table(cls, player_id, minigame, total_games, wins, losses, draws, time_played):
        date_ = f"\"{date.today()}\""
        data = dict()
        row = cls.database.get(
            "players",
            ["total_games", "wins", "losses", "draws", "time_played"],
            {"player_id": player_id, "minigame": minigame, "date": date_},
            1
        )
        if len(row) == 0:
            data["player_id"] = player_id
            data["minigame"] = minigame
            data["date"] = date_
            data["total_games"] = total_games
            data["wins"] = wins
            data["losses"] = losses
            data["draws"] = draws
            data["time_played"] = time_played
            cls.database.write("players", data)
        else:
            row = row[0]
            where = dict()
            where["player_id"] = player_id
            where["minigame"] = minigame
            where["date"] = date_

            data["total_games"] = row["total_games"] + total_games
            data["wins"] = row["wins"] + wins
            data["losses"] = row["losses"] + losses
            data["draws"] = row["draws"] + draws
            data["time_played"] = row["time_played"] + time_played
            cls.database.write("players", data, where)

    @classmethod
    def add_to_minigames_table(cls, server_id, minigame, total_games, wins, losses, draws, time_played):
        date_ = f"\"{date.today()}\""
        data = dict()
        row = cls.database.get(
            "minigames",
            ["total_games", "wins", "losses", "draws", "time_played"],
            {"server_id": server_id, "minigame": minigame, "date": date_},
            1
        )
        if len(row) == 0:
            data["server_id"] = server_id
            data["minigame"] = minigame
            data["date"] = date_
            data["total_games"] = total_games
            data["wins"] = wins
            data["losses"] = losses
            data["draws"] = draws
            data["time_played"] = time_played
            cls.database.write("minigames", data)
        else:
            row = row[0]
            where = dict()
            where["server_id"] = server_id
            where["minigame"] = minigame
            where["date"] = date_

            data["total_games"] = row["total_games"] + total_games
            data["wins"] = row["wins"] + wins
            data["losses"] = row["losses"] + losses
            data["draws"] = row["draws"] + draws
            data["time_played"] = row["time_played"] + time_played
            cls.database.write("minigames", data, where)

    @classmethod
    def get_stats_for_player(cls, player_id):
        return cls.database.get(
            "players",
            ["minigame", "date", "total_games", "wins", "losses", "draws", "time_played"],
            {"player_id": player_id},
        )

    @classmethod
    def get_stats_for_minigame(cls, minigame):
        return cls.database.get(
            "minigames",
            ["server_id", "date", "total_games", "wins", "losses", "draws", "time_played"],
            {"minigame": minigame}
        )

    @classmethod
    def get_stats_for_server(cls, server_id):
        return cls.database.get(
            "minigames",
            ["minigame", "date", "total_games", "wins", "losses", "draws", "time_played"],
            {"server_id": server_id}
        )

    @classmethod
    def query(cls, query):
        return cls.database.query(query)

    @classmethod
    def get_stats_for_minigames(cls):
        return cls.database.get(
            "minigames",
            ["minigame", "date", "total_games", "wins", "losses", "draws", "time_played"],
            {}
        )
