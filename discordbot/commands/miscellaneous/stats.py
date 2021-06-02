import re

from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands.command import Command
from discordbot.utils.pager import Pager


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
        if len(args.split(" ")) <= 1:
            player = context.author
        else:
            player = await cls.bot.fetch_user(int(re.findall(r'\d+', args)[0]))

        pages = []
        stats = cls.bot.db.get_stats_of_player(player.id)
        content = f"Here are the stats for **{player.name}**:"
        content += cls.bot.db.get_formatted_today_stats(stats)
        pages.append(content)

        content = f"Here are the stats for **{player.name}**:"
        content += cls.bot.db.get_formatted_month_stats(stats)
        pages.append(content)

        content = f"Here are the stats for **{player.name}**:"
        content += cls.bot.db.get_formatted_year_stats(stats)
        pages.append(content)

        content = f"Here are the stats for **{player.name}**:"
        content += cls.bot.db.get_formatted_daily_stats(stats)
        pages.append(content)

        content = f"Here are the stats for **{player.name}**:"
        pages.append(cls.bot.db.get_formatted_monthly_stats(stats))
        pages.append(content)

        content = f"Here are the stats for **{player.name}**:"
        pages.append(cls.bot.db.get_formatted_yearly_stats(stats))
        pages.append(content)

        pager = Pager(cls.bot, context.message, pages)
        await pager.show()
        await pager.wait_for_user()
