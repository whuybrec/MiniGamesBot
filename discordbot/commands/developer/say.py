from discordbot.commands.command import Command
from discordbot.private import DISCORD
from discordbot.categories.developer import Developer


class SayCommand(Command):
    bot = None
    name = "say"
    help = "Yeah you know what it does smh..."
    brief = "The bot sends a message that was given as argument."
    args = "*some line*"
    category = Developer

    @classmethod
    async def handler(cls, context, *args: str):
        if cls.has_permission(context.message.author.id):
            content = context.message.content.split(" ")
            content = " ".join(content[1:])
            await context.channel.send(content)
            await context.message.delete()

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
