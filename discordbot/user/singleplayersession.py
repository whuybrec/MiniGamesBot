import datetime
from time import time

from discordbot.managers.databasemanager import DatabaseManager
from discordbot.managers.messagemanager import MessageManager
from discordbot.user.player import Player
from discordbot.user.session import Session
from discordbot.utils.emojis import STOP, REPEAT
from generic.formatting import create_table


class SinglePlayerSession(Session):
    def __init__(self, message, game_name, handler, player):
        super().__init__(message, game_name, handler)
        self.player = Player(player)

    async def pause(self):
        self.stopwatch.pause()
        await MessageManager.edit_message(self.message, self.game.get_board() + "\n" + self.get_summary())

        await MessageManager.add_reaction_and_event(self.message, STOP, self.player.id, self.close)
        await MessageManager.add_reaction_and_event(self.message, REPEAT, self.player.id, self.start_game)

    async def close(self):
        if self.closed:
            return
        self.closed = True
        await MessageManager.clear_reactions(self.message)

        # save data to DB
        stats = self.player.get_stats()
        stats["player_id"] = self.player.id
        stats["minigame"] = f"\"{self.game_name}\""
        stats["time_stamp"] = time()
        stats["time_played"] = self.stopwatch.get_total_time()
        DatabaseManager.add_to_players_table(stats)

        stats.pop("player_id")
        stats["server_id"] = self.message.channel.guild.id
        DatabaseManager.add_to_minigames_table(stats)

    def get_summary(self):
        lst = [["Player", "Wins", "Losses", "Draws", "Unfinished", "Total played"],
               [self.player.name, self.player.wins, self.player.losses, self.player.draws, self.player.unfinished,
                self.player.total_games]]
        table = create_table(*lst)
        summary = \
            f"```\n" \
            f"{table}\n" \
            f"Session Time: {datetime.timedelta(seconds=round(self.stopwatch.get_total_time()))}\n" \
            f"```"
        return summary
