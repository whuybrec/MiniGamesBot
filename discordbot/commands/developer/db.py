import datetime

from discordbot.categories.developer import Developer
from discordbot.commands.command import Command
from discordbot.utils.private import DISCORD
from generic.formatting import creat_table


class DbCommand(Command):
    bot = None
    name = "db"
    help = "fetch some shit here and there."
    brief = "fetch some shit."
    args = "*daily*/*monthly*/*yearly*"
    category = Developer

    @classmethod
    async def handler(cls, context):
        args = context.message.content[len(cls.bot.prefix)+len(cls.name)+1:]
        if cls.has_permission(context.message.author.id):
            if "monthly" in args:
                dict_ = cls.get_monthly_stats()
            elif "yearly" in args:
                dict_ = cls.get_yearly_stats()
            else:
                dict_ = cls.get_daily_stats()
            content = "```\n"
            lists = [["Game", "W", "L", "D", "Total", "Time"], *cls.get_lists_of_dict(dict_)]
            table = creat_table(*lists)
            content += table
            content += "\n```"
            await context.channel.send(content)

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False

    @classmethod
    def get_daily_stats(cls):
        rows = cls.bot.db.get_stats_for_minigames()
        daily = dict()
        for row in rows:
            date_ = datetime.datetime.strptime(row["date"], "%Y-%m-%d")
            if date_.month == datetime.date.today().month \
                    and date_.year == datetime.date.today().year \
                    and date_.day == datetime.date.today().day:
                daily = cls.aggregate_dicts(daily, row)
        return daily

    @classmethod
    def get_monthly_stats(cls):
        rows = cls.bot.db.get_stats_for_minigames()
        monthly = dict()
        for row in rows:
            date_ = datetime.datetime.strptime(row["date"], "%Y-%m-%d")
            if date_.month == datetime.date.today().month and date_.year == datetime.date.today().year:
                monthly = cls.aggregate_dicts(monthly, row)
        return monthly

    @classmethod
    def get_yearly_stats(cls):
        rows = cls.bot.db.get_stats_for_minigames()
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
            lst = [key, value['wins'], value['losses'], value['draws'], value['total_games'],
                   datetime.timedelta(seconds=value['time_played'])]
            lists.append(lst)
        return lists
