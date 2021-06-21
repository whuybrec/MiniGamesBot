from discordbot.messagemanager import MessageManager
from discordbot.discordminigames.singleplayergames.singleplayergame import SinglePlayerGame, WON, LOST, QUIT
from discordbot.utils.emojis import STOP, COLORS as COLORS_EMOJI
from minigames.flood import Flood, COLORS


class FloodDiscord(SinglePlayerGame):
    def __init__(self, session):
        super().__init__(session)
        self.flood_game = Flood()
        self.current_color = COLORS_EMOJI[self.flood_game.grid.matrix[0][0].color]

    async def start_game(self):
        await MessageManager.edit_message(self.message, self.get_board())
        for c in COLORS:
            await MessageManager.add_reaction_and_event(self.message, COLORS_EMOJI[c], self.player.id,
                                                        self.on_color_reaction, COLORS_EMOJI[c])
        await MessageManager.add_reaction_and_event(self.message, STOP, self.player.id, self.on_quit_game)

    async def on_color_reaction(self, color_emoji):
        self.on_start_move()

        if color_emoji == self.current_color:
            return

        await MessageManager.remove_reaction(self.message, self.current_color, self.player.member)
        for color, emoji in COLORS_EMOJI.items():
            if emoji == color_emoji:
                self.flood_game.pick_color(color)
                self.current_color = emoji
                break

        await MessageManager.edit_message(self.message, self.get_board())

        if self.flood_game.has_won():
            await self.game_won()
            return
        elif self.flood_game.has_lost():
            await self.game_lost()
            return

    def get_board(self):
        content = ""
        content += f"Moves left: **{self.flood_game.min_allowed_moves - self.flood_game.player_moves}**\n"
        for i in range(len(self.flood_game.grid.matrix)):
            for j in range(len(self.flood_game.grid.matrix[i])):
                content += COLORS_EMOJI[self.flood_game.grid.matrix[i][j].color]
            content += "\n"

        if self.game_state == WON:
            content += "You have won the game!"
        elif self.game_state == LOST or self.game_state == QUIT:
            content += f"You have lost the game!"
        return content
