from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands.command import Command


class InfoCommand(Command):
    bot = None
    name = "info"
    help = "Shows some information about this bot: donation link, github repo, invite link, invite to my server"
    brief = "Shows some information about this bot."
    args = ""
    category = Miscellaneous

    @classmethod
    async def handler(cls, context):
        text = "Thanks for using MiniGamesBot! :)\n"
        text += "- If you notice any bugs or have any suggestions, then join my server to let me know!\n"
        text += "- Don't forget to give the bot permissions to manage reactions and messages.\n"
        text += "- Leave a reaction or give a thumbs up if you like this bot here: <https://top.gg/bot/704677903182594119>\n"
        text += "- If you wish to make a donation: https://www.buymeacoffee.com/whuybrec\n"
        text += "- Github link: <https://github.com/whuybrec/whuybrec.github.io>\n"
        text += "- Invite to my server: https://discord.gg/hGeGsWp\n"
        await context.message.channel.send(text)
