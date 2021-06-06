import dbl
from discord.ext import commands

from discordbot.utils.private import TOPGG


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""
    def __init__(self, bot):
        self.bot = bot
        self.token = TOPGG["TOKEN"]
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)  # Autopost will post your guild count every 30 minutes

    async def on_guild_post(self):
        print("Server count posted successfully")

