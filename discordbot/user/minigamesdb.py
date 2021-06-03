import calendar
from datetime import date, datetime, timedelta
from time import time
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
                "time_stamp integer",
                "total_games integer",
                "wins integer",
                "losses integer",
                "draws integer",
                "time_played integer"
            ],
            [
                "player_id",
                "minigame",
                "time_stamp"
            ]
        )
        cls.database.create_table(
            "minigames",
            [
                "server_id integer",
                "minigame text",
                "time_stamp integer",
                "total_games",
                "wins integer",
                "losses integer",
                "draws integer",
                "time_played integer"
            ],
            [
                "server_id",
                "minigame",
                "time_stamp"
            ]
        )

    @classmethod
    def add_to_players_table(cls, player_id, minigame, total_games, wins, losses, draws, time_played):
        data = dict()
        data["player_id"] = player_id
        data["minigame"] = minigame
        data["time_stamp"] = time()
        data["total_games"] = total_games
        data["wins"] = wins
        data["losses"] = losses
        data["draws"] = draws
        data["time_played"] = time_played
        cls.database.write("players", data)

    @classmethod
    def add_to_minigames_table(cls, server_id, minigame, total_games, wins, losses, draws, time_played):
        data = dict()
        data["server_id"] = server_id
        data["minigame"] = minigame
        data["time_stamp"] = time()
        data["total_games"] = total_games
        data["wins"] = wins
        data["losses"] = losses
        data["draws"] = draws
        data["time_played"] = time_played
        cls.database.write("minigames", data)

    @classmethod
    def get_all_time_stats_for_player(cls, player_id):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(time_played) " \
            "FROM players " \
            "WHERE player_id={0} " \
            "GROUP BY minigame;".format(player_id)
        return cls.query(q)

    @classmethod
    def get_stats_for_player_of_day(cls, player_id, date_):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(time_played) " \
            "FROM players " \
            "WHERE player_id={0} AND strftime('%Y-%m-%d', time_stamp, 'unixepoch', 'localtime')='{1}' " \
            "GROUP BY minigame;".format(player_id, date_)
        return cls.query(q)

    @classmethod
    def get_stats_for_player_of_month(cls, player_id, date_):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(time_played) " \
            "FROM players " \
            "WHERE player_id={0} AND strftime('%Y-%m', time_stamp, 'unixepoch', 'localtime')='{1}' " \
            "GROUP BY minigame;".format(player_id, date_)
        return cls.query(q)

    @classmethod
    def get_stats_for_player_of_year(cls, player_id, year):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(time_played) " \
            "FROM players " \
            "WHERE player_id={0} AND strftime('%Y', time_stamp, 'unixepoch', 'localtime')='{1}' " \
            "GROUP BY minigame;".format(player_id, year)
        return cls.query(q)

    @classmethod
    def get_all_time_stats_for_minigames(cls):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(time_played) " \
            "FROM minigames " \
            "GROUP BY minigame;"
        return cls.query(q)

    @classmethod
    def get_stats_for_minigames_of_day(cls, date_):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(time_played) " \
            "FROM minigames " \
            "WHERE strftime('%Y-%m-%d', time_stamp, 'unixepoch', 'localtime')='{0}'" \
            "GROUP BY minigame".format(date_)
        return cls.query(q)

    @classmethod
    def get_stats_for_minigames_of_month(cls, date_):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(time_played) " \
            "FROM minigames " \
            "WHERE strftime('%Y-%m', time_stamp, 'unixepoch', 'localtime')='{0}'" \
            "GROUP BY minigame;".format(date_)
        return cls.query(q)

    @classmethod
    def get_stats_for_minigames_of_year(cls, year):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(time_played) " \
            "FROM minigames " \
            "WHERE strftime('%Y', time_stamp, 'unixepoch', 'localtime')='{0}'" \
            "GROUP BY minigame;".format(year)
        return cls.query(q)

    @classmethod
    def get_daily_stats_for_player_of_month(cls, player_id, date_):
        num_days = calendar.monthrange(date_.year, date_.month)[1]
        days = [date(date_.year, date_.month, day) for day in range(1, num_days + 1)]
        stats = dict()
        for day in days:
            stats[day.strftime("%Y-%m-%d")] = cls.get_stats_for_player_of_day(player_id, day.strftime("%Y-%m-%d"))
        return stats

    @classmethod
    def get_monthly_stats_for_player_of_year(cls, player_id, date_):
        months = [date(date_.year, month, 1) for month in range(1, 13)]
        stats = dict()
        for month in months:
            stats[month.strftime("%Y-%m")] = cls.get_stats_for_player_of_month(player_id, month.strftime("%Y-%m"))
        return stats

    @classmethod
    def get_yearly_stats_for_player(cls, player_id, date_):
        years = [date(year, 1, 1) for year in range(date_.year-4, date_.year+1)]
        stats = dict()
        for year in years:
            stats[year.strftime("%Y")] = cls.get_stats_for_player_of_year(player_id, year.strftime("%Y"))
        return stats

    @classmethod
    def get_daily_stats_for_minigames_of_month(cls, date_):
        num_days = calendar.monthrange(date_.year, date_.month)[1]
        days = [date(date_.year, date_.month, day) for day in range(1, num_days + 1)]
        stats = dict()
        for day in days:
            stats[day.strftime("%Y-%m-%d")] = cls.get_stats_for_minigames_of_day(day.strftime("%Y-%m-%d"))
        return stats

    @classmethod
    def get_monthly_stats_for_minigames_of_year(cls, date_):
        months = [date(date_.year, month, 1) for month in range(1, 13)]
        stats = dict()
        for month in months:
            stats[month.strftime("%Y-%m")] = cls.get_stats_for_minigames_of_month(month.strftime("%Y-%m"))
        return stats

    @classmethod
    def get_yearly_stats_for_minigames(cls, date_):
        years = [date(year, 1, 1) for year in range(date_.year - 4, date_.year + 1)]
        stats = dict()
        for year in years:
            stats[year.strftime("%Y")] = cls.get_stats_for_minigames_of_year(year.strftime("%Y"))
        return stats

    @classmethod
    def query(cls, query):
        return cls.database.query(query)

    @classmethod
    def stats_to_list(cls, stats):
        contents = []
        for row in stats:
            contents.append(row["minigame"])
            contents.append(row['wins'])
            contents.append(row['losses'])
            contents.append(row['draws'])
            contents.append(row['total_games'])
            contents.append(row['time_played'])
        return contents

    @classmethod
    async def update(cls):
        channel = await cls.bot.fetch_channel(DISCORD["STATISTICS_CHANNEL"])
        message = await channel.history().flatten()
        try:
            message = message[0]
        except discord.Forbidden and IndexError:
            message = await channel.send("haha brr")

        today = "```diff\n+ Today\n\n"
        lists = [["Game", "W", "L", "D", "Total", "Time"]]
        mg_stats = cls.get_stats_for_minigames_of_day(date.today())
        if mg_stats:
            for row in mg_stats:
                temp = list(tuple(row))
                temp[-1] = timedelta(seconds=int(temp[-1]))
                lists.append(temp)
            table = create_table(*lists)
            today += table
        today += "```"
        today += f"\nServers: **{len(cls.bot.guilds)}**"
        today += f"\nLast edited: **{datetime.now()}**"
        await message.edit(content=today)

        with ZipFile("bin/database_backup.zip", "w") as zip_f:
            zip_f.write(DATABASE_FILE)
        channel = await cls.bot.fetch_channel(DISCORD["STACK_CHANNEL"])
        await channel.send(file=discord.File("bin/database_backup.zip"))
