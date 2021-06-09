from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands.command import Command
from discordbot.utils.emojis import STOP


class InfoCommand(Command):
    bot = None
    name = "info"
    help = "Shows link and information for minigames, statistics, the bot in general."
    brief = "Shows links and information about this bot."
    args = ""
    category = Miscellaneous

    @classmethod
    async def handler(cls, context):
        content = "**__MiniGamesBot__**\n" \
                  "Use the **help command** to see the commands for this bot. " \
                  "Administrators can set a **different prefix** for the bot. " \
                  "Use the **bug command** to notify me for potential bugs. " \
                  "You can also **join my server** to tell me about it in there. "
        content += "\n\n**__Minigames__**\n" \
                   "All the minigames are played by **clicking reactions** the bot added. " \
                   f"The game automatically results in **loss** if user clicks {STOP} or has not reacted after **5 minutes**. " \
                   "Use the **rules command** to check out the rules for a minigame. " \
                   "There are currently 2 multiplayer games: connect4 & chess. "
        content += "\n\n**__Statistics__**\n" \
                   "This bot tracks the following per **player statistics** for all minigames: " \
                   "**wins**, **losses**, **draws**, **total games**, **unfinished games**, **total time played**. " \
                   "Unfinished games is the portion of losses where the 5 minute timer got reached. " \
                   "Use the **stats command** to ask for yours or another player's stats. " \
                   "Use the arrows to navigate through the **different periods**. "
        content += "\n\n**__Links__**\n" \
                   "Bot invite link: <https://discord.com/oauth2/authorize?client_id=704677903182594119&permissions=305216&scope=bot>\n" \
                   "Leave a reaction or give a thumbs up if you like this bot here: <https://top.gg/bot/704677903182594119>\n" \
                   "If you wish to make a donation: https://www.buymeacoffee.com/whuybrec\n" \
                   "Github link: <https://github.com/whuybrec/whuybrec.github.io>\n" \
                   "Invite to my server: https://discord.gg/hGeGsWp\n"
        await context.send(content)
