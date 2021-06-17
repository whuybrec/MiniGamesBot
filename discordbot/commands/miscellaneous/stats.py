import re

from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands.command import Command
from discordbot.utils.pager import Pager


class StatsCommand(Command):
    bot = None
    name = "stats"
    help = "Shows yours (if no player was tagged as argument) or another player's statistics for all minigames."
    brief = "Shows stats for all minigames."
    args = "*@player*"
    category = Miscellaneous

    @classmethod
    async def invoke(cls, context):
        args = context.message.content[len(cls.bot.prefix) + len(cls.name) + 1:].lstrip()
        if len(args.lstrip()) > 0:
            player = await cls.bot.fetch_user(int(re.findall(r'\d+', args)[0]))
        else:
            player = context.author

        pages = []
        table = cls.bot.db.get_formatted_stats_for_today_of_player(player.id)
        pages.append(f"Stats of today for **{player.name}**:\n```\n{table}\n```")

        table = cls.bot.db.get_formatted_weekly_stats_of_player(player.id)
        pages.append(f"Weekly stats for **{player.name}**:\n```\n{table}\n```")

        table = cls.bot.db.get_formatted_monthly_stats_of_player(player.id)
        pages.append(f"Monthly stats for **{player.name}**:\n```\n{table}\n```")

        table = cls.bot.db.get_formatted_yearly_stats_of_player(player.id)
        pages.append(f"Yearly stats for **{player.name}**:\n```\n{table}\n```")

        pager = Pager(cls.bot, context, pages)
        await pager.show()
        await pager.wait_for_user()
