from Commands.discord_command import DiscordCommand
from Other.private import Private

class SayCommand(DiscordCommand):
    bot = None
    name = "say"
    help = "The bot sends a message that was given as argument."
    brief = "The bot sends a message that was given as argument."
    usage = ""
    category = "developer"

    @classmethod
    async def handler(cls, context, *args: str):
        if context.message.author.id in Private.DEV_IDS.keys():
            await context.channel.send(context.message.content[len("?say "):])
            await context.message.delete()
