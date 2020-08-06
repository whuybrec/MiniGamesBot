from Commands.discord_command import DiscordCommand
from Other.variables import Variables

class InfoCommand(DiscordCommand):
    bot = None
    name = "info"
    help = "Displays some information about the bot."
    brief = "Displays some information about the bot."
    usage = ""
    category = "miscellaneous"

    @classmethod
    async def handler(cls, context, *args, **kwargs):
        text = "- Check out my github page with the source code, you can sponsor me there too.\n"
        text += "- If you notice any bugs or have any suggestions, " \
                "don't hesitate to use the bug command and request command!\n"
        text += "- Don't forget to give the bot permissions to manage reactions and messages.\n"
        text += "- Press " + Variables.STOP_EMOJI + " to close the game.\n"
        text += "- Every minigame has a time limit of " + str(int(Variables.DEADLINE/60)) + " minutes.\n"
        text += "- You can find the invite link to this bot on this page: <https://top.gg/bot/704677903182594119>\n"
        text += "- If you wish to make a donation: https://www.buymeacoffee.com/whuybrec\n"
        text += "- Github link: <https://github.com/whuybrec/whuybrec.github.io>\n"
        await context.message.channel.send(text)

