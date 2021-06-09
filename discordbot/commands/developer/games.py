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

            lists = [["Game", "W", "L", "D", "Total", "Diff", "Unfinished", "Time"]]
            avg_stats = cls.bot.db.get_average_played_minigames_of_month(today)
            mg_stats = cls.bot.db.get_stats_for_minigames_of_day(today)
            if mg_stats:
                for row in mg_stats:
                    temp = list(tuple(row))
                    temp.insert(5, "")

                    for avg_row in avg_stats:
                        avg_row_ = tuple(avg_row)
                        if avg_row_[0] == temp[0]:
                            percentage = round(((temp[4]/avg_row_[1])-1)*100)
                            if percentage < 0:
                                temp[5] = f"{percentage}%"
                            elif percentage > 0:
                                temp[5] = f"+{percentage}%"
                            else:
                                temp[5] = f"~"

                    temp[-1] = timedelta(seconds=int(temp[-1]))
                    lists.append(temp)
                pages.append("Stats for today:\n```\n" + create_table(*lists) + "\n```")

            lists = [["Week", "Game", "W", "L", "D", "Total", "Unfinished", "Time"]]
            mg_weekly_stats = cls.bot.db.get_weekly_stats_for_minigames_of_month(today)
            weeks = [date(today.year, today.month, day) for day in range(1, 31, 7)]
            for week in weeks:
                if mg_weekly_stats[week.strftime("%W")]:
                    mg_stats = mg_weekly_stats[week.strftime("%W")]
                    lists.append([week.strftime("%W"), "", "", "", "", "", "", ""])
                    for row in mg_stats:
                        temp = list(tuple(row))
                        temp.insert(0, "")
                        temp[-1] = timedelta(seconds=int(temp[-1]))
                        lists.append(temp)
            pages.append("Weekly stats:\n```\n"+create_table(*lists)+"\n```")

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
