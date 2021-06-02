from discordbot.categories.developer import Developer
from discordbot.commands.command import Command
from discordbot.utils.pager import Pager
from discordbot.utils.private import DISCORD


class DbCommand(Command):
    bot = None
    name = "db"
    help = "fetch ALL OF THE DATA."
    brief = "ALL OF THE DATA."
    args = ""
    category = Developer

    @classmethod
    async def handler(cls, context):
        if cls.has_permission(context.message.author.id):
            pages = []
            stats = cls.bot.db.get_stats_of_minigames()
            pages.append(cls.bot.db.get_formatted_today_stats(stats))
            pages.append(cls.bot.db.get_formatted_month_stats(stats))
            pages.append(cls.bot.db.get_formatted_year_stats(stats))
            pages.append(cls.bot.db.get_formatted_daily_stats(stats))
            pages.append(cls.bot.db.get_formatted_monthly_stats(stats))
            pages.append(cls.bot.db.get_formatted_yearly_stats(stats))
            pager = Pager(cls.bot, context.message, pages)
            await pager.show()
            await pager.wait_for_user()

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
