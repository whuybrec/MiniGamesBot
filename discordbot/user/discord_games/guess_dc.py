from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.emojis import STOP, COLORS as COLORS_EMOJI, ARROW_LEFT, CHECKMARK, REPEAT
from minigames.mastermind import Mastermind, COLORS


class MastermindDisc(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.mastermind = Mastermind()
        self.code = []

    async def start(self):
        await self.session.message.edit(content=self.get_content())
        for c in COLORS:
            await self.add_reaction(COLORS_EMOJI[c])
        await self.add_reaction(ARROW_LEFT)
        await self.add_reaction(CHECKMARK)
        await self.add_reaction(STOP)
        await self.wait_for_player()

    async def on_reaction(self, reaction, user):
        if reaction.emoji == ARROW_LEFT:
            await self.session.message.remove_reaction(ARROW_LEFT, user)
            try:
                color = self.code[-1]
                await self.session.message.remove_reaction(COLORS_EMOJI[color], user)
                self.code.remove(color)
                await self.session.message.edit(content=self.get_content())
                return
            except IndexError:
                pass

        for color, e in COLORS_EMOJI.items():
            if e == reaction.emoji and color not in self.code:
                self.code.append(color)

        if reaction.emoji == CHECKMARK:
            await self.session.message.remove_reaction(CHECKMARK, user)
            if len(self.code) == 4:
                self.mastermind.guess(self.code)
                for color in self.code:
                    await self.session.message.remove_reaction(COLORS_EMOJI[color], user)
                self.code = []

        if self.mastermind.has_won():
            self.winners.append(self.players[0])
            self.playing = False
        elif self.mastermind.has_lost():
            self.losers.append(self.players[0])
            self.playing = False

        await self.session.message.edit(content=self.get_content())

    def get_content(self):
        content = f"Lives: {self.mastermind.lives}\nYour guess:"
        for code in self.code:
            content += COLORS_EMOJI[code]
        content += "\n\n"

        if len(self.mastermind.history) > 0:
            for history_ in self.mastermind.history:
                for color in history_[0]:
                    content += COLORS_EMOJI[color]
                content += "  "
                content += CHECKMARK * history_[1]
                content += REPEAT * history_[2]
                content += "\n"
        if not self.playing:
            if len(self.winners) == 1:
                content += "You have won the game!"
            else:
                content += f"You have lost the game!\nThe code was: "
                for color in self.mastermind.code:
                    content += COLORS_EMOJI[color]
        return content
