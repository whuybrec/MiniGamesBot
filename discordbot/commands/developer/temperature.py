from gpiozero import CPUTemperature

from discordbot.categories.developer import Developer
from discordbot.commands.command import Command
from discordbot.utils.private import DISCORD


class TemperatureCommand(Command):
    bot = None
    name = "temp"
    help = "Shows the temperature o- UGH why do I even bother..."
    brief = "Shows the temperature of the raspberry pi"
    args = ""
    category = Developer

    @classmethod
    async def invoke(cls, context):
        if cls.has_permission(context.message.author.id):
            await context.channel.send(str(CPUTemperature().temperature) + "°C")

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
