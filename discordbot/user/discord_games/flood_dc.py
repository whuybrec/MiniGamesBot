from discordbot.messagemanager import MessageManager
from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.emojis import STOP, COLORS as COLORS_EMOJI
from minigames.flood import Flood, COLORS


class FloodDiscord(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.flood_game = Flood()
        self.current_color = COLORS_EMOJI[self.flood_game.grid.matrix[0][0].color]
        self.player = self.session.players[0]

    async def start_game(self):
        await MessageManager.edit_message(self.message, self.get_content())

        for c in COLORS:
            await MessageManager.add_reaction_event(self.message, COLORS_EMOJI[c], self.player.id,
                                                    self.on_color_reaction, COLORS_EMOJI[c])
        await MessageManager.add_reaction_event(self.message, STOP, self.player.id, self.on_stop_reaction)

        self.start_timer()

    async def on_color_reaction(self, color_emoji):
        self.cancel_timer()

        if color_emoji == self.current_color:
            return

        await MessageManager.remove_reaction(self.message, self.current_color, self.player.member)
        for color, emoji in COLORS_EMOJI.items():
            if emoji == color_emoji:
                self.flood_game.pick_color(color)
                self.current_color = emoji
                break

        if self.flood_game.has_won():
            self.player.wins += 1
            await self.end_game()
            return
        elif self.flood_game.has_lost():
            self.player.losses += 1
            await self.end_game()
            return

        self.start_timer()
        await MessageManager.edit_message(self.message, self.get_content())

    def get_content(self):
        content = ""
        content += f"Moves left: **{self.flood_game.min_allowed_moves - self.flood_game.player_moves}**\n"
        for i in range(len(self.flood_game.grid.matrix)):
            for j in range(len(self.flood_game.grid.matrix[i])):
                content += COLORS_EMOJI[self.flood_game.grid.matrix[i][j].color]
            content += "\n"
        if self.finished:
            if self.flood_game.has_won():
                content += "You have won the game!"
            else:
                content += f"You have lost the game!"
        return content
