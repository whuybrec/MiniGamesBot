from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands.command import Command


class RulesCommand(Command):
    bot = None
    name = "rules"
    help = "Shows the rules for the minigame given as argument to the command."
    brief = "Shows for the a given minigame."
    args = "*minigame*"
    category = Miscellaneous

    @classmethod
    async def handler(cls, context):
        await context.message.channel.send("I NEED TO DO THIS")
