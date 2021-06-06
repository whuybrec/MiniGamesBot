import datetime
import time

from discord import Message
from discord.ext.commands import Context

from discordbot.user.gamemanager import GameManager


class Session:
    def __init__(self, bot, context: Context, message: Message, minigame_name, minigame_callback, players, extra=False):
        self.bot = bot
        self.context = context
        self.message = message
        self.minigame_name = minigame_name
        self.minigame_callback = minigame_callback
        self.players = players
        self.extra = extra

        self.amount = 0
        self.start_time = 0
        self.session_time = 0
        self.minigame = None
        self.message_extra = None
        self.player_timed_out = None
        self.stats_players = dict()
        for player in self.players:
            self.stats_players[player.id] = {
                "wins": 0,
                "losses": 0,
                "draws": 0
            }

    async def start(self):
        self.amount += 1
        self.start_time = time.time()
        if self.extra and self.message_extra is None:
            self.message_extra = await self.message.channel.send("** **")
        await self.message.clear_reactions()

        self.minigame = self.minigame_callback.__call__(self)
        await self.minigame.start()

    async def close(self):
        await self.message.clear_reactions()
        if self.extra:
            await self.message_extra.clear_reactions()

        if len(self.minigame.winners) == 0 or len(self.minigame.losers) == 0 or len(self.minigame.drawers) == 0:
            return

        # save data to DB
        wins = losses = draws = 0
        for pid, stats in self.stats_players.items():
            wins += stats["wins"]
            losses += stats["losses"]
            draws += stats["draws"]
            if self.player_timed_out is not None and self.player_timed_out == pid:
                self.bot.db.add_to_players_table(
                    pid,
                    f"\"{self.minigame_name}\"",
                    self.amount,
                    stats["wins"],
                    stats["losses"],
                    stats["draws"],
                    self.session_time,
                    True
                )
            else:
                self.bot.db.add_to_players_table(
                    pid,
                    f"\"{self.minigame_name}\"",
                    self.amount,
                    stats["wins"],
                    stats["losses"],
                    stats["draws"],
                    self.session_time,
                    False
                )

        if self.player_timed_out is not None:
            timeout = True
        else:
            timeout = False

        self.bot.db.add_to_minigames_table(
            self.context.guild.id,
            f"\"{self.minigame_name}\"",
            self.amount,
            wins,
            losses,
            draws,
            self.session_time,
            timeout
        )

    async def pause(self):
        self.session_time += round(time.time() - self.start_time)
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
        summary += f"\nSession Time: {datetime.timedelta(seconds=self.session_time)}```"
        return summary
