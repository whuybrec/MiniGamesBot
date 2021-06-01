import re

from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands.command import Command
from generic.formatting import creat_table
import datetime


class StatsCommand(Command):
    bot = None
    name = "stats"
    help = "Shows yours or another player's stats for all minigames."
    brief = "Shows stats for all minigames."
    args = "*<player>*"
    category = Miscellaneous

    @classmethod
    async def handler(cls, context):
        args = context.message.content[len(cls.bot.prefix) + len(cls.name) + 1:]
        if len(args) == 0:
            player = context.author
        else:
            player = await cls.bot.fetch_user(int(re.findall(r'\d+', args)[0]))

        stats = cls.bot.db.get_stats_for_player(player.id)

        content = f"```\n{player.name}\n\n"
        lists = [["Period", "Game", "W", "L", "D", "Total", "Time"],
                 ["Today", "", "", "", "", "", ""],
                 *cls.get_lists_of_dict(cls.get_day_stats(stats)),
                 ["Month", "", "", "", "", "", ""],
                 *cls.get_lists_of_dict(cls.get_month_stats(stats)),
                 ["Year", "", "", "", "", "", ""],
                 *cls.get_lists_of_dict(cls.get_year_stats(stats))
                 ]
        table = creat_table(*lists)
        content += table
        content += "\n```"
        await context.channel.send(content)

    @classmethod
    def get_day_stats(cls, rows):
        daily = dict()
        for row in rows:
            date_ = datetime.datetime.strptime(row["date"], "%Y-%m-%d")
            if date_.month == datetime.date.today().month \
                    and date_.year == datetime.date.today().year \
                    and date_.day == datetime.date.today().day:
                daily = cls.aggregate_dicts(daily, row)
        return daily

    @classmethod
    def get_month_stats(cls, rows):
        monthly = dict()
        for row in rows:
            date_ = datetime.datetime.strptime(row["date"], "%Y-%m-%d")
            if date_.month == datetime.date.today().month and date_.year == datetime.date.today().year:
                monthly = cls.aggregate_dicts(monthly, row)
        return monthly

    @classmethod
    def get_year_stats(cls, rows):
        yearly = dict()
        for row in rows:
            date_ = datetime.datetime.strptime(row["date"], "%Y-%m-%d")
            if date_.year == datetime.date.today().year:
                yearly = cls.aggregate_dicts(yearly, row)
        return yearly

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
            lst = ["", key, value['wins'], value['losses'], value['draws'], value['total_games'], datetime.timedelta(seconds=value['time_played'])]
            lists.append(lst)
        return lists
