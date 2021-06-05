from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands.command import Command
from discordbot.utils.private import DISCORD


class SetPrefixCommand(Command):
    bot = None
    name = "set_prefix"
    help = "Set a new prefix for this bot, prefix must be shorter than 10 characters."
    brief = "Set a new prefix for this bot."
    args = "new prefix"
    category = Miscellaneous

    @classmethod
    async def handler(cls, context):
        if not context.channel.permissions_for(context.author).administrator and context.author.id not in DISCORD["DEVS"]:
            await context.reply("Only admins can change the prefix of the bot.")
            return

        prefix = context.message.content[len(cls.bot.prefix) + len(cls.name) + 1:].lstrip()
        if len(prefix) == 0:
            await context.reply("You need to provide a new prefix.")
            return

        if len(prefix) > 10:
            await context.reply("Prefix can not be longer than 10 characters.")
            return

        cls.bot.prefixes[str(context.guild.id)] = prefix
        await cls.bot.save_prefixes()
        await context.reply(f"The prefix of MiniGamesBot is now: **{prefix}**")
