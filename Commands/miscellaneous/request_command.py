from Commands.discord_command import DiscordCommand
from Other.private import Private


class RequestCommand(DiscordCommand):
    bot = None
    name = "request"
    help = "If you have an idea for a new minigame or existing minigame, let me know via this command." \
           "Pass the idea as argument to this command."
    brief = "You have an idea for a new or existing minigame."
    usage = "[description of idea]"
    category = "miscellaneous"

    @classmethod
    async def handler(cls, context, *args: str):
        if not args:
            return

        request = " ".join(args)
        channel = cls.bot.get_channel(Private.SUGGESTIONS_CHANNELID)
        await channel.send(context.author.name + " REQUESTS: " + request + "\n"
                           + "id: " + str(context.author.id) + "\n"
                           + "guild: " + str(context.guild.id) + "\n"
                           + "channel: " + str(context.channel.id) + "\n")
        channel = cls.bot.get_channel(Private.PUBLIC_SUGGESTIONS_CHANNELID)
        await channel.send(context.author.name + " requests: \"" + request + "\"")
        await context.channel.send("Request succesfully delivered!")
