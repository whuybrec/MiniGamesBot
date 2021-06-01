from discordbot.categories.developer import Developer
from discordbot.commands.command import Command
from discordbot.utils.private import DISCORD


class DeleteCommand(Command):
    bot = None
    name = "delete"
    help = "It should be pretty damn clear you boomer...."
    brief = "Deletes the message with given msg id."
    args = "*message_id*"
    category = Developer

    @classmethod
    async def handler(cls, context):
        args = context.message.content[len(cls.bot.prefix)+len(cls.name)+1:]

        if cls.has_permission(context.message.author.id):
            msg = await context.message.channel.fetch_message(int(args))
            await msg.delete()
            await context.message.delete()

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
