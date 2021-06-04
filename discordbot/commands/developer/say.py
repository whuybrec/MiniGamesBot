from discordbot.categories.developer import Developer
from discordbot.commands.command import Command
from discordbot.utils.private import DISCORD


class SayCommand(Command):
    bot = None
    name = "say"
    help = "Yeah you know what it does smh..."
    brief = "The bot sends a message that was given as argument."
    args = "some line"
    category = Developer

    @classmethod
    async def handler(cls, context):
        args = context.message.content[len(cls.bot.prefix) + len(cls.name) + 1:].lstrip()
        if cls.has_permission(context.message.author.id):
            await context.channel.send(args)
            await context.message.delete()

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
