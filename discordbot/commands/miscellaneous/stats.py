import calendar
from datetime import date, timedelta
import re

from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands.command import Command
from discordbot.utils.pager import Pager
from generic.formatting import create_table


class StatsCommand(Command):
    bot = None
    name = "stats"
    help = "Shows yours (if no player was tagged as argument) or another player's statistics for all minigames."
    brief = "Shows stats for all minigames."
    args = "*player*"
    category = Miscellaneous

    @classmethod
    async def handler(cls, context):
        args = context.message.content[len(cls.bot.prefix) + len(cls.name) + 1:]
        if len(args.lstrip()) > 0:
            player = await cls.bot.fetch_user(int(re.findall(r'\d+', args)[0]))
        else:
            player = context.author

        pages = []
        today = date.today()
        lists = [["Game", "W", "L", "D", "Total", "Time"]]
        mg_stats = cls.bot.db.get_stats_for_player_of_day(player.id, today)
        if mg_stats:
            for row in mg_stats:
                temp = list(tuple(row))
                temp[-1] = timedelta(seconds=int(temp[-1]))
                lists.append(temp)
            pages.append(f"Stats of today for **{player.name}**:\n```\n" + create_table(*lists) + "\n```")

        lists = [["Game", "W", "L", "D", "Total", "Time"]]
        mg_stats = cls.bot.db.get_stats_for_player_of_month(player.id, today.strftime("%Y-%m"))
        if mg_stats:
            for row in mg_stats:
                temp = list(tuple(row))
                temp[-1] = timedelta(seconds=int(temp[-1]))
                lists.append(temp)
            pages.append(f"Stats of this month for **{player.name}**:\n```\n" + create_table(*lists) + "\n```")

        lists = [["Game", "W", "L", "D", "Total", "Time"]]
        mg_stats = cls.bot.db.get_stats_for_player_of_year(player.id, today.year)
        if mg_stats:
            for row in mg_stats:
                temp = list(tuple(row))
                temp[-1] = timedelta(seconds=int(temp[-1]))
                lists.append(temp)
            pages.append(f"Stats of this year for **{player.name}**:\n```\n" + create_table(*lists) + "\n```")

        lists = [["Day", "Game", "W", "L", "D", "Total", "Time"]]
        mg_daily_stats = cls.bot.db.get_daily_stats_for_player_of_month(player.id, today)
        num_days = calendar.monthrange(today.year, today.month)[1]
        days = [date(today.year, today.month, day) for day in range(1, num_days + 1)]
        for day in days:
            if mg_daily_stats[day.strftime("%Y-%m-%d")]:
                mg_stats = mg_daily_stats[day.strftime("%Y-%m-%d")]
                lists.append([day.day, "", "", "", "", "", ""])
                for row in mg_stats:
                    temp = list(tuple(row))
                    temp.insert(0, "")
                    temp[-1] = timedelta(seconds=int(temp[-1]))
                    lists.append(temp)
        pages.append(f"Daily stats for **{player.name}**:\n```\n" + create_table(*lists) + "\n```")

        lists = [["Month", "Game", "W", "L", "D", "Total", "Time"]]
        mg_monthly_stats = cls.bot.db.get_monthly_stats_for_player_of_year(player.id, today)
        months = [date(today.year, month, 1) for month in range(1, 13)]
        for month in months:
            if mg_monthly_stats[month.strftime("%Y-%m")]:
                mg_stats = mg_monthly_stats[month.strftime("%Y-%m")]
                lists.append([month.strftime("%B"), "", "", "", "", "", ""])
                for row in mg_stats:
                    temp = list(tuple(row))
                    temp.insert(0, "")
                    temp[-1] = timedelta(seconds=int(temp[-1]))
                    lists.append(temp)
        pages.append(f"Monthly stats for **{player.name}**:\n```\n" + create_table(*lists) + "\n```")

        lists = [["Year", "Game", "W", "L", "D", "Total", "Time"]]
        mg_yearly_stats = cls.bot.db.get_yearly_stats_for_player(player.id, today)
        years = [date(year, 1, 1) for year in range(today.year - 4, today.year + 1)]
        for year in years:
            if mg_yearly_stats[year.strftime("%Y")]:
                mg_stats = mg_yearly_stats[year.strftime("%Y")]
                lists.append([year.year, "", "", "", "", "", ""])
                for row in mg_stats:
                    temp = list(tuple(row))
                    temp.insert(0, "")
                    temp[-1] = timedelta(seconds=int(temp[-1]))
                    lists.append(temp)
        pages.append(f"Yearly stats for **{player.name}**:\n```\n" + create_table(*lists) + "\n```")

        pager = Pager(cls.bot, context.message, pages)
        await pager.show()
        await pager.wait_for_user()
