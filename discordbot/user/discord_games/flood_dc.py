from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.emojis import STOP, COLORS as COLORS_EMOJI
from minigames.flood import Flood, COLORS


class FloodDisc(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.flood_game = Flood()

    async def start(self):
        await self.session.message.edit(content=self.get_content())
        for c in COLORS:
            await self.add_reaction(COLORS_EMOJI[c])
        await self.add_reaction(STOP)
        await self.wait_for_player()

    async def on_reaction(self, reaction, user):
        for color, e in COLORS_EMOJI.items():
            if e == reaction.emoji:
                self.flood_game.pick_color(color)
                await self.session.message.remove_reaction(e, user)
                break

        if self.flood_game.has_won():
            self.winners.append(self.players[0])
            self.playing = False
        elif self.flood_game.has_lost():
            self.losers.append(self.players[0])
            self.playing = False

        await self.session.message.edit(content=self.get_content())

    def get_content(self):
        content = ""
        content += f"Moves left: **{self.flood_game.min_allowed_moves - self.flood_game.player_moves}**\n"
        content += f"Min moves: {self.flood_game.min_moves}\n"
        for i in range(len(self.flood_game.grid.matrix)):
            for j in range(len(self.flood_game.grid.matrix[i])):
                content += COLORS_EMOJI[self.flood_game.grid.matrix[i][j].color]
            content += "\n"
        if not self.playing:
            if len(self.winners) == 1:
                content += "You have won the game!"
            else:
                content += f"You have lost the game!"
        return content
