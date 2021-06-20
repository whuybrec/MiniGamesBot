import datetime
from time import time

from discordbot.databasemanager import DatabaseManager
from discordbot.messagemanager import MessageManager
from discordbot.user.player import Player
from discordbot.user.session import Session
from discordbot.utils.emojis import STOP, REPEAT
from generic.formatting import create_table


class MultiPlayerSession(Session):
    def __init__(self, message, game_name, handler, *players):
        super().__init__(message, game_name, handler)
        self.players = [Player(player) for player in players]

    async def pause(self):
        self.stopwatch.pause()
        await MessageManager.edit_message(self.message, self.game.get_board() + "\n" + self.get_summary())

        for player in self.players:
            await MessageManager.add_reaction_event(self.message, STOP, player.id, self.close)
            await MessageManager.add_reaction_event(self.message, REPEAT, player.id, self.start_game)

    async def close(self):
        if self.closed:
            return

        self.closed = True
        await MessageManager.clear_reactions(self.message)

        # save data to DB
        for player in self.players:
            stats = player.get_stats()
            stats["player_id"] = player.id
            stats["minigame"] = f"\"{self.game_name}\""
            stats["time_stamp"] = time()
            stats["time_played"] = self.stopwatch.get_total_time()
            DatabaseManager.add_to_players_table(stats)

        stats = {
            "server_id": self.message.channel.guild.id,
            "minigame": f"\"{self.game_name}\"",
            "time_stamp": time(),
            "wins": self.players[0].wins + self.players[1].wins,
            "losses": self.players[0].losses + self.players[1].losses,
            "draws": self.players[0].draws,
            "unfinished": self.players[0].unfinished,
            "total_games": self.players[0].total_games,
            "time_played": self.stopwatch.get_total_time()
        }
        DatabaseManager.add_to_minigames_table(stats)

    async def send_extra_message(self):
        if self.extra_message is None:
            self.extra_message = await self.message.channel.send("** **")
            self.game.extra_message = self.extra_message

    def get_summary(self):
        lst = [["Player", "Wins", "Losses", "Draws", "Unfinished", "Total played"]]
        for player in self.players:
            lst.append([player.name, player.wins, player.losses, player.draws, player.unfinished, player.total_games])
        table = create_table(*lst)
        summary = \
            f"```\n" \
            f"{table}\n" \
            f"Session Time: {datetime.timedelta(seconds=round(self.stopwatch.get_total_time()))}\n" \
            f"```"
        return summary
