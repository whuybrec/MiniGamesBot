from Commands.discord_command import DiscordCommand
from Other.private import Private


class RequestCommand(DiscordCommand):
    bot = None
    name = "request"
    help = "If you have an idea for a new minigame or for an existing minigame, let me know via this command." \
           "Pass the idea as argument to this command."
    brief = "Report a bug to the developer with a description as argument."
    usage = "[description of idea]"
    category = "miscellaneous"

    @classmethod
    async def handler(cls, context, *args: str, **kwargs):
        if not args:
            return

        report = args[0]
        channel = cls.bot.get_channel(Private.USER_REPORTS_CHANNELID)
        if report is None:
            await context.channel.send("Not allowed to send empty request, try: ?request [your text here]")
            return
        await channel.send(context.author.name + " REQUESTS: " + report + "\n"
                           + "id: " + str(context.author.id) + "\n"
                           + "guild: " + str(context.guild.id) + "\n"
                           + "channel: " + str(context.channel.id) + "\n")
        await context.channel.send("Request succesfully delivered!")
