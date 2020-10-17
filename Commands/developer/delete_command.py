from Commands.discord_command import DiscordCommand
from Other.private import Private

class DeleteCommand(DiscordCommand):
    bot = None
    name = "delete"
    help = "Deletes the message with given msg id."
    brief = "Deletes the message with given msg id."
    usage = ""
    category = "developer"

    @classmethod
    async def handler(cls, context, *args: int):
        if context.message.author.id in Private.DEV_IDS.keys():
            msg = await context.message.channel.fetch_message(args[0])
            await msg.delete()
            await context.message.delete()
