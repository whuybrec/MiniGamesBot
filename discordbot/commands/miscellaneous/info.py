from ..command import Command
from discordbot.categories.miscellaneous import Miscellaneous


class InfoCommand(Command):
    bot = None
    name = "info"
    help = "Shows some information about this bot: donation link, github repo, invite link, invite to my server"
    brief = "Shows some information about this bot."
    args = ""
    category = Miscellaneous

    @classmethod
    async def handler(cls, context, *args):
        text = "Thanks for using MiniGamesBot! :)"
        text += "- Check out my github page with the source code.\n"
        text += "- If you notice any bugs or have any suggestions, " \
                "don't hesitate to use the bug command and request command or just tell me in my server (link below)!\n"
        text += "- Don't forget to give the bot permissions to manage reactions and messages.\n"
        text += "- You can find the invite link to this bot on this page: <https://top.gg/bot/704677903182594119>\n"
        text += "- If you wish to make a donation: https://www.buymeacoffee.com/whuybrec\n"
        text += "- Github link: <https://github.com/whuybrec/whuybrec.github.io>\n"
        text += "- Invite to my server: https://discord.gg/hGeGsWp\n"
        await context.message.channel.send(text)
