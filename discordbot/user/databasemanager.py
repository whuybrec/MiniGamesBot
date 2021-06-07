import calendar
from datetime import date, datetime, timedelta
from time import time
from zipfile import ZipFile

import discord

from discordbot.utils.private import DISCORD
from generic.database import Database
from generic.formatting import create_table

DATABASE_FILE = "bin/minigames.db"


class DatabaseManager:
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
                "wins integer",
                "losses integer",
                "draws integer",
                "total_games integer",
                "time_played integer",
                "timeout boolean"
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
                "wins integer",
                "losses integer",
                "draws integer",
                "total_games",
                "time_played integer",
                "timeout boolean"
            ],
            [
                "server_id",
                "minigame",
                "time_stamp"
            ]
        )

        cls.database.create_table(
            "servers",
            [
                "server_id integer",
                "time_stamp integer",
                "event text"
            ],
            [
                "server_id",
                "time_stamp",
            ]
        )

    @classmethod
    def add_to_players_table(cls, player_id, minigame, total_games, wins, losses, draws, time_played, timeout):
        data = dict()
        data["player_id"] = player_id
        data["minigame"] = minigame
        data["time_stamp"] = time()
        data["wins"] = wins
        data["losses"] = losses
        data["draws"] = draws
        data["total_games"] = total_games
        data["time_played"] = time_played
        data["timeout"] = timeout
        cls.database.write("players", data)

    @classmethod
    def add_to_minigames_table(cls, server_id, minigame, total_games, wins, losses, draws, time_played, timeout):
        data = dict()
        data["server_id"] = server_id
        data["minigame"] = minigame
        data["time_stamp"] = time()
        data["wins"] = wins
        data["losses"] = losses
        data["draws"] = draws
        data["total_games"] = total_games
        data["time_played"] = time_played
        data["timeout"] = timeout
        cls.database.write("minigames", data)

    @classmethod
    def add_to_servers_table(cls, server_id, event):
        data = dict()
        data["server_id"] = server_id
        data["time_stamp"] = time()
        data["event"] = event
        cls.database.write("servers", data)

    # PLAYERS

    @classmethod
    def get_all_time_stats_for_player(cls, player_id):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(timeout), SUM(time_played) " \
            "FROM players " \
            "WHERE player_id={0} " \
            "GROUP BY minigame;".format(player_id)
        return cls.query(q)

    @classmethod
    def get_stats_for_player_of_day(cls, player_id, date_):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(timeout), SUM(time_played) " \
            "FROM players " \
            "WHERE player_id={0} AND strftime('%Y-%m-%d', time_stamp, 'unixepoch', 'localtime')='{1}' " \
            "GROUP BY minigame;".format(player_id, date_)
        return cls.query(q)

    @classmethod
    def get_stats_for_player_of_week(cls, player_id, date_):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(timeout), SUM(time_played) " \
            "FROM players " \
            "WHERE player_id={0} AND strftime('%W', time_stamp, 'unixepoch', 'localtime')='{1}'" \
            "GROUP BY minigame".format(player_id, date_.strftime('%W'))
        return cls.query(q)

    @classmethod
    def get_stats_for_player_of_month(cls, player_id, date_):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(timeout), SUM(time_played) " \
            "FROM players " \
            "WHERE player_id={0} AND strftime('%Y-%m', time_stamp, 'unixepoch', 'localtime')='{1}' " \
            "GROUP BY minigame;".format(player_id, date_)
        return cls.query(q)

    @classmethod
    def get_stats_for_player_of_year(cls, player_id, year):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(timeout), SUM(time_played) " \
            "FROM players " \
            "WHERE player_id={0} AND strftime('%Y', time_stamp, 'unixepoch', 'localtime')='{1}' " \
            "GROUP BY minigame;".format(player_id, year)
        return cls.query(q)

    @classmethod
    def get_weekly_stats_for_player_of_month(cls, player_id, date_):
        weeks = [date(date_.year, date_.month, day) for day in range(1, 31, 7)]
        stats = dict()
        for week in weeks:
            stats[week.strftime("%W")] = cls.get_stats_for_player_of_week(player_id, week)
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

    # MINIGAMES

    @classmethod
    def get_all_time_stats_for_minigames(cls):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(timeout), SUM(time_played) " \
            "FROM minigames " \
            "GROUP BY minigame;"
        return cls.query(q)

    @classmethod
    def get_stats_for_minigames_of_day(cls, date_):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(timeout), SUM(time_played) " \
            "FROM minigames " \
            "WHERE strftime('%Y-%m-%d', time_stamp, 'unixepoch', 'localtime')='{0}'" \
            "GROUP BY minigame".format(date_.strftime('%Y-%m-%d'))
        return cls.query(q)

    @classmethod
    def get_stats_for_minigames_of_week(cls, date_):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(timeout), SUM(time_played) " \
            "FROM minigames " \
            "WHERE strftime('%W', time_stamp, 'unixepoch', 'localtime')='{0}'" \
            "GROUP BY minigame".format(date_.strftime('%W'))
        return cls.query(q)

    @classmethod
    def get_stats_for_minigames_of_month(cls, date_):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(timeout), SUM(time_played) " \
            "FROM minigames " \
            "WHERE strftime('%Y-%m', time_stamp, 'unixepoch', 'localtime')='{0}'" \
            "GROUP BY minigame;".format(date_.strftime('%Y-%m'))
        return cls.query(q)

    @classmethod
    def get_stats_for_minigames_of_year(cls, date_):
        q = "SELECT minigame, SUM(wins), SUM(losses), SUM(draws), SUM(total_games), SUM(timeout), SUM(time_played) " \
            "FROM minigames " \
            "WHERE strftime('%Y', time_stamp, 'unixepoch', 'localtime')='{0}'" \
            "GROUP BY minigame;".format(date_.strftime('%Y'))
        return cls.query(q)

    @classmethod
    def get_average_played_minigames_of_month(cls, date_):
        q = "SELECT minigame, AVG(total_games) " \
            "FROM (" \
            "   SELECT minigame, SUM(total_games) as 'total_games', time_stamp as 'time_stamp' " \
            "   FROM minigames " \
            "   GROUP BY minigame, strftime('%Y-%m', time_stamp, 'unixepoch', 'localtime')" \
            ") " \
            "WHERE strftime('%Y-%m', time_stamp, 'unixepoch', 'localtime')='{0}' " \
            "GROUP BY minigame;".format(date_.strftime('%Y-%m'))
        return cls.query(q)

    @classmethod
    def get_weekly_stats_for_minigames_of_month(cls, date_):
        weeks = [date(date_.year, date_.month, day) for day in range(1, 31, 7)]
        stats = dict()
        for week in weeks:
            stats[week.strftime("%W")] = cls.get_stats_for_minigames_of_week(week)
        return stats

    @classmethod
    def get_monthly_stats_for_minigames_of_year(cls, date_):
        months = [date(date_.year, month, 1) for month in range(1, 13)]
        stats = dict()
        for month in months:
            stats[month.strftime("%Y-%m")] = cls.get_stats_for_minigames_of_month(month)
        return stats

    @classmethod
    def get_yearly_stats_for_minigames(cls, date_):
        years = [date(year, 1, 1) for year in range(date_.year - 4, date_.year + 1)]
        stats = dict()
        for year in years:
            stats[year.strftime("%Y")] = cls.get_stats_for_minigames_of_year(year)
        return stats

    # SERVERS

    @classmethod
    def get_servers_of_day(cls, event, date_):
        q = "SELECT server_id " \
            "FROM servers " \
            "WHERE event='{0}' AND strftime('%Y-%m-%d', time_stamp, 'unixepoch', 'localtime')='{1}' " \
            "GROUP BY server_id;".format(event, date_)
        return cls.query(q)

    @classmethod
    def get_servers_of_month(cls, event, date_):
        q = "SELECT server_id " \
            "FROM servers " \
            "WHERE event='{0}' AND strftime('%Y-%m', time_stamp, 'unixepoch', 'localtime')='{1}' " \
            "GROUP BY server_id;".format(event, date_)
        return cls.query(q)

    @classmethod
    def get_servers_of_year(cls, event, year):
        q = "SELECT server_id " \
            "FROM servers " \
            "WHERE event='{0}' AND strftime('%Y', time_stamp, 'unixepoch', 'localtime')='{1}' " \
            "GROUP BY server_id;".format(event, year)
        return cls.query(q)

    @classmethod
    def get_daily_stats_for_servers_of_month(cls, event, date_):
        num_days = calendar.monthrange(date_.year, date_.month)[1]
        days = [date(date_.year, date_.month, day) for day in range(1, num_days + 1)]
        stats = dict()
        for day in days:
            stats[day.strftime("%Y-%m-%d")] = cls.get_servers_of_day(event, day.strftime("%Y-%m-%d"))
        return stats

    @classmethod
    def get_monthly_stats_for_servers_of_year(cls, event, date_):
        months = [date(date_.year, month, 1) for month in range(1, 13)]
        stats = dict()
        for month in months:
            stats[month.strftime("%Y-%m")] = cls.get_servers_of_month(event, month.strftime("%Y-%m"))
        return stats

    @classmethod
    def get_yearly_stats_for_servers(cls, event, date_):
        years = [date(year, 1, 1) for year in range(date_.year - 4, date_.year + 1)]
        stats = dict()
        for year in years:
            stats[year.strftime("%Y")] = cls.get_servers_of_year(event, year.strftime("%Y"))
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
        lists = [["Game", "W", "L", "D", "Total", "Diff", "Unfinished", "Time"]]
        avg_stats = cls.bot.db.get_average_played_minigames_of_month(date.today())
        mg_stats = cls.get_stats_for_minigames_of_day(date.today())
        if mg_stats:
            for row in mg_stats:
                temp = list(tuple(row))
                temp.insert(5, "")
                for avg_row in avg_stats:
                    avg_row_ = tuple(avg_row)
                    if avg_row_[0] == temp[0]:
                        percentage = round(((temp[4] / avg_row_[1]) - 1) * 100)
                        if percentage < 0:
                            temp[5] = f"{percentage}%"
                        elif percentage > 0:
                            temp[5] = f"+{percentage}%"
                        else:
                            temp[5] = f"~"

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
        channel = await cls.bot.fetch_channel(DISCORD["BACKUP_CHANNEL"])
        await channel.send(file=discord.File("bin/database_backup.zip"))
