from datetime import date, datetime, timedelta
from zipfile import ZipFile

import discord

from discordbot.utils.private import DISCORD
from generic.database import Database
from generic.formatting import create_table

DATABASE_FILE = "bin/minigames.db"


class MinigamesDB:
    database: Database
    bot = None

    @classmethod
    def on_startup(cls, bot):
        cls.bot = bot
        cls.database = Database(DATABASE_FILE)
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
        date_1 = date.today()
        date_1 = date_1.replace(year=2018)
        date_ = f"\"{date_1}\""
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
        date_1 = date.today()
        date_1 = date_1.replace(year=2018)
        date_ = f"\"{date_1}\""
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
    def get_stats_of_player(cls, player_id):
        return cls.database.get(
            "players",
            ["minigame", "date", "total_games", "wins", "losses", "draws", "time_played"],
            {"player_id": player_id},
        )

    @classmethod
    def get_stats_of_minigame(cls, minigame):
        return cls.database.get(
            "minigames",
            ["server_id", "date", "total_games", "wins", "losses", "draws", "time_played"],
            {"minigame": minigame}
        )

    @classmethod
    def get_stats_of_server(cls, server_id):
        return cls.database.get(
            "minigames",
            ["minigame", "date", "total_games", "wins", "losses", "draws", "time_played"],
            {"server_id": server_id}
        )

    @classmethod
    def query(cls, query):
        return cls.database.query(query)

    @classmethod
    def get_stats_of_minigames(cls):
        return cls.database.get(
            "minigames",
            ["minigame", "date", "total_games", "wins", "losses", "draws", "time_played"],
            {}
        )

    @classmethod
    def get_stats_for_day(cls, rows, date_):
        return cls.get_daily_stats(rows, date_)[date_.strftime("%d/%m")]

    @classmethod
    def get_stats_for_month(cls, rows, date_):
        return cls.get_monthly_stats(rows)[date_.strftime("%B")]

    @classmethod
    def get_stats_for_year(cls, rows, date_1):
        stats = dict()
        for row in rows:
            date_2 = datetime.strptime(row["date"], "%Y-%m-%d")
            if date_2.year == date_1.year:
                stats = cls.aggregate_dicts(stats, row)
        return stats

    @classmethod
    def get_daily_stats(cls, rows, date_1):
        daily = dict()
        for i in range(30):
            stats = dict()
            for row in rows:
                date_2 = datetime.strptime(row["date"], "%Y-%m-%d")
                if date_2.day == date_1.day and date_2.month == date_1.month and date_2.year == date_1.year:
                    stats = cls.aggregate_dicts(stats, row)
            daily[date_1.strftime("%d/%m")] = stats
            date_1 = date_1 - timedelta(days=1)
        return daily

    @classmethod
    def get_monthly_stats(cls, rows):
        monthly = dict()
        date_1 = date(2021, 1, 1)
        for i in range(12):
            stats = dict()
            for row in rows:
                date_2 = datetime.strptime(row["date"], "%Y-%m-%d")
                if date_2.month == date_1.month and date_2.year == date_1.year:
                    stats = cls.aggregate_dicts(stats, row)
            monthly[date_1.strftime("%B")] = stats
            date_1 = date_1 + timedelta(days=32)
            date_1 = date_1.replace(day=1)
        return monthly

    @classmethod
    def get_yearly_stats(cls, rows, date_1):
        daily = dict()
        start_year = date_1.year
        for i in range(5):
            date_1 = date_1.replace(year=start_year-i)
            stats = dict()
            for row in rows:
                date_2 = datetime.strptime(row["date"], "%Y-%m-%d")
                if date_2.year == date_1.year:
                    stats = cls.aggregate_dicts(stats, row)
            daily[date_1.year] = stats
        return daily

    @classmethod
    def aggregate_dicts(cls, dict_, row):
        if row["minigame"] in dict_.keys():
            dict_[row["minigame"]]["wins"] += row["wins"]
            dict_[row["minigame"]]["losses"] += row["losses"]
            dict_[row["minigame"]]["draws"] += row["draws"]
            dict_[row["minigame"]]["total_games"] += row["total_games"]
            dict_[row["minigame"]]["time_played"] += row["time_played"]
        else:
            dict_[row["minigame"]] = dict()
            dict_[row["minigame"]]["wins"] = row["wins"]
            dict_[row["minigame"]]["losses"] = row["losses"]
            dict_[row["minigame"]]["draws"] = row["draws"]
            dict_[row["minigame"]]["total_games"] = row["total_games"]
            dict_[row["minigame"]]["time_played"] = row["time_played"]
        return dict_

    @classmethod
    def get_lists_of_dict(cls, dict_):
        lists = []
        for key, value in dict_.items():
            lst = [key, value['wins'], value['losses'], value['draws'], value['total_games'],
                   timedelta(seconds=value['time_played'])]
            lists.append(lst)
        return lists

    @classmethod
    def get_lists_of_daily_dict(cls, dict_):
        lists = [["Day", "Game", "W", "L", "D", "Total", "Time"]]
        date_1 = date.today()
        for i in range(30):
            if len(dict_[date_1.strftime("%d/%m")]) != 0:
                lists.append([date_1.strftime("%d/%m"), "", "", "", "", "", ""])
                for lst in cls.get_lists_of_dict(dict_[date_1.strftime("%d/%m")]):
                    lst.insert(0, "")
                    lists.append(lst)
            date_1 = date_1 - timedelta(days=1)
        return lists

    @classmethod
    def get_lists_of_monthly_dict(cls, dict_):
        lists = [["Month", "Game", "W", "L", "D", "Total", "Time"]]
        date_1 = date(2021, 1, 1)
        for i in range(12):
            if len(dict_[date_1.strftime("%B")]) != 0:
                lists.append([date_1.strftime("%B"), "", "", "", "", "", ""])
                for lst in cls.get_lists_of_dict(dict_[date_1.strftime("%B")]):
                    lst.insert(0, "")
                    lists.append(lst)
            date_1 = date_1 + timedelta(days=32)
            date_1 = date_1.replace(day=1)
        return lists

    @classmethod
    def get_lists_of_yearly_dict(cls, dict_):
        lists = [["Year", "Game", "W", "L", "D", "Total", "Time"]]
        date_1 = date.today()
        start_year = date_1.year
        for i in range(5):
            date_1 = date_1.replace(year=start_year - i)
            if len(dict_[date_1.year]) != 0:
                lists.append([date_1.year, "", "", "", "", "", ""])
                for lst in cls.get_lists_of_dict(dict_[date_1.year]):
                    lst.insert(0, "")
                    lists.append(lst)
        return lists

    @classmethod
    def get_formatted_today_stats(cls, stats):
        content = "```diff\n+ Today\n\n"
        dict_ = cls.get_stats_for_day(stats, date.today())
        lists = [["Game", "W", "L", "D", "Total", "Time"], *cls.get_lists_of_dict(dict_)]
        content += create_table(*lists)
        content += "\n```"
        return content

    @classmethod
    def get_formatted_month_stats(cls, stats):
        content = "```diff\n+ This Month\n\n"
        dict_ = cls.get_stats_for_month(stats, date.today())
        lists = [["Game", "W", "L", "D", "Total", "Time"], *cls.get_lists_of_dict(dict_)]
        content += create_table(*lists)
        content += "\n```"
        return content

    @classmethod
    def get_formatted_year_stats(cls, stats):
        content = "```diff\n+ This Year\n\n"
        dict_ = cls.get_stats_for_year(stats, date.today())
        lists = [["Game", "W", "L", "D", "Total", "Time"], *cls.get_lists_of_dict(dict_)]
        content += create_table(*lists)
        content += "\n```"
        return content

    @classmethod
    def get_formatted_daily_stats(cls, stats):
        content = "```diff\n+ Daily\n\n"
        dict_ = cls.get_daily_stats(stats, date.today())
        lists = cls.get_lists_of_daily_dict(dict_)
        content += create_table(*lists)
        content += "\n```"
        return content

    @classmethod
    def get_formatted_monthly_stats(cls, stats):
        content = "```diff\n+ Monthly\n\n"
        dict_ = cls.get_monthly_stats(stats)
        lists = cls.get_lists_of_monthly_dict(dict_)
        content += create_table(*lists)
        content += "\n```"
        return content

    @classmethod
    def get_formatted_yearly_stats(cls, stats):
        content = "```diff\n+ Yearly\n\n"
        dict_ = cls.get_yearly_stats(stats, date.today())
        lists = cls.get_lists_of_yearly_dict(dict_)
        content += create_table(*lists)
        content += "\n```"
        return content

    @classmethod
    async def update(cls):
        channel = await cls.bot.fetch_channel(DISCORD["STATISTICS_CHANNEL"])
        message = await channel.history().flatten()
        try:
            message = message[0]
        except discord.Forbidden and IndexError:
            message = await channel.send("haha brr")
        stats = cls.get_stats_of_minigames()
        today = cls.get_formatted_today_stats(stats)
        today += f"\nLast edited: **{datetime.now()}**"
        await message.edit(content=today)

        with ZipFile("bin/database_backup.zip", "w") as zip_f:
            zip_f.write(DATABASE_FILE)
        channel = await cls.bot.fetch_channel(DISCORD["STACK_CHANNEL"])
        await channel.send(file=discord.File("bin/database_backup.zip"))
