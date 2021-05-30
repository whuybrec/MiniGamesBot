import datetime
import time

from discord import Message
from discord.ext.commands import Context

from discordbot.user.gamemanager import GameManager


class Session:
    def __init__(self, bot, context: Context, message: Message, minigame_callback, players):
        self.bot = bot
        self.context = context
        self.message = message
        self.minigame_callback = minigame_callback
        self.players = players

        self.start_time = 0
        self.session_time = 0
        self.minigame = None
        self.message_extra = None
        self.stats_players = dict()
        for player in self.players:
            self.stats_players[player.id] = {
                "wins": 0,
                "losses": 0,
                "draws": 0
            }

    async def start(self):
        self.start_time = time.time()
        if self.message_extra is None:
            self.message_extra = await self.message.channel.send("** **")
        await self.message.clear_reactions()

        self.minigame = self.minigame_callback.__call__(self)
        await self.minigame.start()

    async def close(self):
        await self.message.clear_reactions()
        if self.message_extra is not None:
            await self.message_extra.clear_reactions()
        # save data to DB

    async def pause(self):
        self.session_time += time.time() - self.start_time
        self.start_time = 0

        await GameManager.pause_session(self)

    def get_summary(self):
        summary = "```\n"
        max_ = max([len(p.name) for p in self.players]) + 1
        summary += f"{' '.ljust(max_)}{'Wins'.rjust(5)}{'Losses'.rjust(7)}{'Draws'.rjust(6)}\n"
        for player in self.players:
            res = self.stats_players[player.id]
            summary += f"{player.name.ljust(max_)}" \
                       f"{str(res['wins']).rjust(5)}" \
                       f"{str(res['losses']).rjust(7)}" \
                       f"{str(res['draws']).rjust(6)}\n"
        summary += f"\nSession Time: {datetime.timedelta(seconds=round(self.session_time))}```"
        return summary
