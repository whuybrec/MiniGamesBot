from gpiozero import CPUTemperature
from Commands.discord_command import DiscordCommand
from Other.private import Private

class TemperatureCommand(DiscordCommand):
    bot = None
    name = "temp"
    help = "Sends the temperature of the device running the bot"
    brief = "Sends the temperature of the device running the bot"
    usage = ""
    category = "developer"

    @classmethod
    async def handler(cls, context, *args, **kwargs):
        if context.message.author.id in Private.DEV_IDS.keys():
            await context.channel.send(str(CPUTemperature().temperature) + "°C")

