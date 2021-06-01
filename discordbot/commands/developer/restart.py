import sys

from discordbot.categories.developer import Developer
from discordbot.commands.command import Command
from discordbot.utils.private import DISCORD


class RestartCommand(Command):

    name: str = "restart"
    help: str = "Restart MiniGamesBot"
    brief: str = "Beep boop bop, cya later"
    args: str = ""
    category: str = Developer

    @classmethod
    async def handler(cls, context):
        if not cls.has_permission(context.message.author.id):
            return
        await context.message.channel.send(f"Be right back!\n")
        print("See you soon...")
        sys.exit()

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
