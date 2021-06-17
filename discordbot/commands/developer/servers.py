import calendar
from datetime import date

from discordbot.categories.developer import Developer
from discordbot.commands.command import Command
from discordbot.utils.pager import Pager
from discordbot.utils.private import DISCORD
from generic.formatting import create_table


class ServersCommand(Command):
    bot = None
    name = "servers"
    help = "fetch server join/leave data."
    brief = "fetch server join/leave data."
    args = ""
    category = Developer

    @classmethod
    async def invoke(cls, context):
        if cls.has_permission(context.message.author.id):
            pages = []
            today = date.today()

            lists = [["Day", "Joined", "Left", "Diff"]]
            joined_servers = cls.bot.db.get_daily_stats_for_servers_of_month("JOIN", today)
            left_servers = cls.bot.db.get_daily_stats_for_servers_of_month("LEAVE", today)
            num_days = calendar.monthrange(today.year, today.month)[1]
            days = [date(today.year, today.month, day) for day in range(1, num_days + 1)]
            for day in days:
                joined_on_day = joined_servers[day.strftime("%Y-%m-%d")]
                left_on_day = left_servers[day.strftime("%Y-%m-%d")]
                if len(joined_on_day) != 0 or len(left_on_day) != 0:
                    lists.append([day.strftime("%d-%m"), len(joined_on_day), len(left_on_day), len(joined_on_day)-len(left_on_day)])
            pages.append("Daily:\n```\n" + create_table(*lists) + "\n```\nCurrent total: **" + str(len(cls.bot.guilds)) + "**")

            lists = [["Month", "Joined", "Left", "Diff"]]
            joined_servers = cls.bot.db.get_monthly_stats_for_servers_of_year("JOIN", today)
            left_servers = cls.bot.db.get_monthly_stats_for_servers_of_year("LEAVE", today)
            months = [date(today.year, month, 1) for month in range(1, 13)]
            for month in months:
                joined_on_month = joined_servers[month.strftime("%Y-%m")]
                left_on_month = left_servers[month.strftime("%Y-%m")]
                if len(joined_on_month) != 0 or len(left_on_month) != 0:
                    lists.append([month.strftime("%B"), len(joined_on_month), len(left_on_month), len(joined_on_month)-len(left_on_month)])
            pages.append("Monthly:\n```\n" + create_table(*lists) + "\n```\nCurrent total: **" + str(len(cls.bot.guilds)) + "**")

            lists = [["Year", "Joined", "Left", "Diff"]]
            joined_servers = cls.bot.db.get_yearly_stats_for_servers("JOIN", today)
            left_servers = cls.bot.db.get_yearly_stats_for_servers("LEAVE", today)
            years = [date(year, 1, 1) for year in range(today.year - 4, today.year + 1)]
            for year in years:
                joined_on_year = joined_servers[year.strftime("%Y")]
                left_on_year = left_servers[year.strftime("%Y")]
                if len(joined_on_year) != 0 or len(left_on_year) != 0:
                    lists.append([year.year, len(joined_on_year), len(left_on_year), len(joined_on_year)-len(left_on_year)])
            pages.append("Yearly:\n```\n" + create_table(*lists) + "\n```\nCurrent total: **" + str(len(cls.bot.guilds)) + "**")

            pager = Pager(cls.bot, context, pages)
            await pager.show()
            await pager.wait_for_user()

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
