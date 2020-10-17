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
    async def handler(cls, context, *args):
        text = "- Check out my github page with the source code, you can sponsor me there too.\n"
        text += "- If you notice any bugs or have any suggestions, " \
                "don't hesitate to use the bug command and request command or just tell me in my server (link below)!\n"
        text += "- Don't forget to give the bot permissions to manage reactions and messages.\n"
        text += "- You can find the invite link to this bot on this page: <https://top.gg/bot/704677903182594119>\n"
        text += "- If you wish to make a donation: https://www.buymeacoffee.com/whuybrec\n"
        text += "- Github link: <https://github.com/whuybrec/whuybrec.github.io>\n"
        text += "- Invite to my server: https://discord.gg/hGeGsWp\n"
        await context.message.channel.send(text)

