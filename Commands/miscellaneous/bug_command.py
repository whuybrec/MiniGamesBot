from Commands.discord_command import DiscordCommand
from Other.private import Private

class BugCommand(DiscordCommand):
    bot = None
    name = "bug"
    help = "If you found a bug in a minigame, then you can report it to the developer. " \
           "Give detailed information (an image is possible) as argument so the bug can be resolved quickly."
    brief = "Report a bug to the developer with a description as argument."
    usage = "[description of bug]"
    category = "miscellaneous"

    @classmethod
    async def handler(cls, context, *args: str):
        if not args:
            return

        bug = " ".join(args)
        channel = cls.bot.get_channel(Private.BUGS_CHANNELID)
        try:
            picture = context.message.attachments[0].url
            await channel.send(picture)
        except:
            pass
        await channel.send(context.author.name + " REPORTS: " + bug + "\n"
                           + "id: " + str(context.author.id) + "\n"
                           + "guild: " + str(context.guild.id) + "\n"
                           + "channel: " + str(context.channel.id) + "\n")
        channel = cls.bot.get_channel(Private.PUBLIC_BUGS_CHANNELID)
        await channel.send(context.author.name + " reports: \"" + bug + "\"")
        await context.channel.send("Bug succesfully reported!")
