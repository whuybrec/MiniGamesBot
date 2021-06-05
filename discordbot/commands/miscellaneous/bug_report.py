from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands.command import Command
from discordbot.utils.private import DISCORD


class BugCommand(Command):
    bot = None
    name = "bug"
    help = "If you found a bug, then you can report it to the developer. Please give detailed information (an image is possible) as argument so the bug can be resolved quickly."
    brief = "Report a bug with a description as argument."
    args = "description"
    category = Miscellaneous

    @classmethod
    async def handler(cls, context):
        bug = context.message.content[len(cls.bot.prefix) + len(cls.name) + 1:].lstrip()
        if len(bug) == 0:
            await context.reply("You need to provide a bug description.")
            return

        channel = cls.bot.get_channel(DISCORD["BUG_REPORT_CHANNEL"])
        try:
            picture = context.message.attachments[0].url
            await channel.send(picture)
        except Exception as e:
            print(e)
            pass
        await channel.send(context.author.name + " REPORTS: " + bug + "\n"
                           + "id: " + str(context.author.id) + "\n"
                           + "guild: " + str(context.guild.id) + "\n"
                           + "channel: " + str(context.channel.id) + "\n")
        await context.reply("Bug successfully reported!")
