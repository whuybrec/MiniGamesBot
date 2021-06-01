import re

from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands.command import Command
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
        daily = cls.get_day_stats(stats)
        monthly = cls.get_month_stats(stats)
        yearly = cls.get_year_stats(stats)
        content = f"```\n{player.name}\n\n"
        content += "Period".ljust(8) + "Game".ljust(10) + "W".rjust(4) + "L".rjust(4) + "D".rjust(4) + "Total".rjust(7) + "Time".rjust(9) + "\n"
        content += f"Today\n"
        content += cls.format_content(daily)
        content += f"\nMonth\n"
        content += cls.format_content(monthly)
        content += f"\nYear\n"
        content += cls.format_content(yearly)
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
    def format_content(cls, dict_):
        content = ""
        for key, value in dict_.items():
            content += "".ljust(8) \
                       + key.ljust(10) \
                       + str(value['wins']).rjust(4) \
                       + str(value['losses']).rjust(4) \
                       + str(value['draws']).rjust(4) \
                       + str(value['total_games']).rjust(7) \
                       + str(datetime.timedelta(seconds=value['time_played'])).rjust(9) + "\n"
        return content
