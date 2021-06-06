import calendar
from datetime import date, timedelta

from discordbot.categories.developer import Developer
from discordbot.commands.command import Command
from discordbot.utils.pager import Pager
from discordbot.utils.private import DISCORD
from generic.formatting import create_table


class GamesCommand(Command):
    bot = None
    name = "games"
    help = "Shows minigames statistics."
    brief = "ALL OF THE DATA."
    args = ""
    category = Developer

    @classmethod
    async def handler(cls, context):
        if cls.has_permission(context.message.author.id):
            pages = []
            today = date.today()

            lists = [["Game", "W", "L", "D", "Total", "Unfinished", "Time"]]
            mg_stats = cls.bot.db.get_stats_for_minigames_of_day(today)
            if mg_stats:
                for row in mg_stats:
                    temp = list(tuple(row))
                    temp[-1] = timedelta(seconds=int(temp[-1]))
                    lists.append(temp)
                pages.append("Stats for today:\n```\n" + create_table(*lists) + "\n```")

            lists = [["Game", "W", "L", "D", "Total", "Unfinished", "Time"]]
            mg_stats = cls.bot.db.get_stats_for_minigames_of_month(today.strftime("%Y-%m"))
            if mg_stats:
                for row in mg_stats:
                    temp = list(tuple(row))
                    temp[-1] = timedelta(seconds=int(temp[-1]))
                    lists.append(temp)
                pages.append("Stats for this month:\n```\n" + create_table(*lists) + "\n```")

            lists = [["Game", "W", "L", "D", "Total", "Unfinished", "Time"]]
            mg_stats = cls.bot.db.get_stats_for_minigames_of_year(today.year)
            if mg_stats:
                for row in mg_stats:
                    temp = list(tuple(row))
                    temp[-1] = timedelta(seconds=int(temp[-1]))
                    lists.append(temp)
                pages.append("Stats for this year:\n```\n" + create_table(*lists) + "\n```")

            lists = [["Day", "Game", "W", "L", "D", "Total", "Unfinished", "Time"]]
            mg_daily_stats = cls.bot.db.get_daily_stats_for_minigames_of_month(today)
            num_days = calendar.monthrange(today.year, today.month)[1]
            days = [date(today.year, today.month, day) for day in range(1, num_days + 1)]
            for day in days:
                if mg_daily_stats[day.strftime("%Y-%m-%d")]:
                    mg_stats = mg_daily_stats[day.strftime("%Y-%m-%d")]
                    lists.append([day.strftime("%d-%m"), "", "", "", "", "", "", ""])
                    for row in mg_stats:
                        temp = list(tuple(row))
                        temp.insert(0, "")
                        temp[-1] = timedelta(seconds=int(temp[-1]))
                        lists.append(temp)
            pages.append("Daily stats:\n```\n"+create_table(*lists)+"\n```")

            lists = [["Month", "Game", "W", "L", "D", "Total", "Unfinished", "Time"]]
            mg_monthly_stats = cls.bot.db.get_monthly_stats_for_minigames_of_year(today)
            months = [date(today.year, month, 1) for month in range(1, 13)]
            for month in months:
                if mg_monthly_stats[month.strftime("%Y-%m")]:
                    mg_stats = mg_monthly_stats[month.strftime("%Y-%m")]
                    lists.append([month.strftime("%B"), "", "", "", "", "", "", ""])
                    for row in mg_stats:
                        temp = list(tuple(row))
                        temp.insert(0, "")
                        temp[-1] = timedelta(seconds=int(temp[-1]))
                        lists.append(temp)
            pages.append("Monthly stats:\n```\n" + create_table(*lists) + "\n```")

            lists = [["Year", "Game", "W", "L", "D", "Total", "Unfinished", "Time"]]
            mg_yearly_stats = cls.bot.db.get_yearly_stats_for_minigames(today)
            years = [date(year, 1, 1) for year in range(today.year - 4, today.year + 1)]
            for year in years:
                if mg_yearly_stats[year.strftime("%Y")]:
                    mg_stats = mg_yearly_stats[year.strftime("%Y")]
                    lists.append([year.year, "", "", "", "", "", "", ""])
                    for row in mg_stats:
                        temp = list(tuple(row))
                        temp.insert(0, "")
                        temp[-1] = timedelta(seconds=int(temp[-1]))
                        lists.append(temp)
            pages.append("Yearly stats:\n```\n" + create_table(*lists) + "\n```")

            pager = Pager(cls.bot, context, pages)
            await pager.show()
            await pager.wait_for_user()

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
