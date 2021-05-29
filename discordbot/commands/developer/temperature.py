from gpiozero import CPUTemperature
from discordbot.commands.command import Command
from discordbot.private import DISCORD
from discordbot.categories.developer import Developer


class TemperatureCommand(Command):
    bot = None
    name = "temp"
    help = "Shows the temperature o- UGH why do I even bother..."
    brief = "Shows the temperature of the raspberry pi"
    args = ""
    category = Developer

    @classmethod
    async def handler(cls, context, *args):
        if cls.has_permission(context.message.author.id):
            await context.channel.send(str(CPUTemperature().temperature) + "°C")

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
