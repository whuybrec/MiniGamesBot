from discordbot.categories.developer import Developer
from discordbot.commands.command import Command
from discordbot.utils.private import DISCORD


class ClearCommand(Command):
    bot = None
    name = "clear"
    help = "SKIBIDI BOP MM DADA"
    brief = "Deletes the last x messages in this channel."
    args = "amount"
    category = Developer

    @classmethod
    async def handler(cls, context):
        args = context.message.content[len(cls.bot.prefix) + len(cls.name) + 1:].lstrip()
        try:
            if cls.has_permission(context.message.author.id):
                await context.channel.purge(limit=int(args))
        except Exception as e:
            print(e)
            await context.channel.send("Yeah you fucked up mate.")

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False

