from discordbot.categories.developer import Developer
from discordbot.commands.command import Command
from discordbot.utils.pager import Pager
from discordbot.utils.private import DISCORD


class GamesCommand(Command):
    bot = None
    name = "games"
    help = "Shows minigames statistics."
    brief = "ALL OF THE DATA."
    args = ""
    category = Developer

    @classmethod
    async def invoke(cls, context):
        if cls.has_permission(context.message.author.id):
            pages = []

            table = cls.bot.db.get_formatted_stats_for_today_of_minigames()
            pages.append(f"Stats of today:\n```\n{table}\n```")

            table = cls.bot.db.get_formatted_weekly_stats_of_minigames()
            pages.append(f"Weekly stats:\n```\n{table}\n```")

            table = cls.bot.db.get_formatted_monthly_stats_of_minigames()
            pages.append(f"Monthly stats:\n```\n{table}\n```")

            table = cls.bot.db.get_formatted_yearly_stats_of_minigames()
            pages.append(f"Yearly stats:\n```\n{table}\n```")

            pager = Pager(cls.bot, context, pages)
            await pager.show()
            await pager.wait_for_user()

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
