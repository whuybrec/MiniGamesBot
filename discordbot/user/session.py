import datetime

from discordbot.messagemanager import MessageManager
from discordbot.user.player import Player
from discordbot.utils.emojis import STOP, REPEAT
from generic.formatting import create_table
from generic.stopwatch import Stopwatch

TIMEOUT = 20


class Session:
    def __init__(self, game_manager, message, minigame_name, *players):
        self.game_manager = game_manager
        self.scheduler = self.game_manager.scheduler
        self.message = message
        self.extra_message = None
        self.minigame_name = minigame_name
        self.players = list()
        for player in players:
            self.players.append(Player(player))

        self.games_played = 0
        self.ticket = None
        self.minigame = None
        self.stopwatch = Stopwatch()
        self.restart = False

    async def start(self):
        self.stopwatch.start()

        self.minigame = self.game_manager.minigames[self.minigame_name](self)
        self.games_played += 1

        try:
            await self.minigame.start_game()
        except Exception as e:
            await self.game_manager.bot.on_error(self.minigame_name, e)
            await self.close()

    async def continue_(self):
        self.game_manager.scheduler.cancel(self.ticket)
        await MessageManager.clear_reactions(self.message)

        if self.game_manager.bot.has_update:
            await MessageManager.edit_message(self.message,
                                              "Sorry! I can't start any new games right now. Boss says I have to restart soon:tm:. Try again later!")
            await self.close()
            return

        await self.start()

    async def pause(self):
        self.stopwatch.pause()
        self.ticket = self.game_manager.scheduler.add(TIMEOUT, self.close)

        for player in self.players:
            await MessageManager.add_reaction_event(self.message, STOP, player.id, self.close)
            await MessageManager.add_reaction_event(self.message, REPEAT, player.id, self.continue_)

    async def close(self):
        self.game_manager.scheduler.cancel(self.ticket)
        await MessageManager.clear_reactions(self.message)

        # save data to DB
        wins = losses = draws = 0
        timeout = False
        for player in self.players:
            wins += player.wins
            losses += player.losses
            draws += player.draws
            timeout = timeout or player.is_idle()
            self.game_manager.add_player_stats_to_db(
                player.id, f"\"{self.minigame_name}\"", self.games_played,
                player.wins, player.losses, player.draws,
                self.stopwatch.get_total_time(),
                player.is_idle()
            )

        self.game_manager.add_minigame_stats_to_db(
            self.message.channel.guild.id, f"\"{self.minigame_name}\"", self.games_played,
            wins, losses, draws,
            self.stopwatch.get_total_time(),
            timeout
        )

        self.game_manager.close_session(self)

    async def on_bot_restart(self):
        await self.minigame.on_bot_restart()
        await self.close()

    async def send_extra_message(self):
        if self.extra_message is None:
            self.extra_message = await self.message.channel.send("** **")
            self.minigame.extra_message = self.extra_message

    def get_summary(self):
        summary = "```\n"
        lst = [["Player", "Wins", "Losses", "Draws", "Total played"]]
        for player in self.players:
            lst.append([player.name, player.wins, player.losses, player.draws, self.games_played])
        table = create_table(*lst)
        summary += table
        summary += f"\nSession Time: {datetime.timedelta(seconds=self.stopwatch.get_total_time())}\n```"
        return summary
