from discordbot.messagemanager import MessageManager
from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.emojis import STOP, COLORS as COLORS_EMOJI, ARROW_LEFT, CHECKMARK, REPEAT
from minigames.mastermind import Mastermind, COLORS


class MastermindDiscord(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.mastermind = Mastermind()
        self.player = self.session.players[0]
        self.code = []

    async def start_game(self):
        await MessageManager.edit_message(self.message, self.get_content())

        for c in COLORS:
            await MessageManager.add_reaction_event(self.message, COLORS_EMOJI[c], self.player.id,
                                                    self.on_color_reaction, COLORS_EMOJI[c])
        await MessageManager.add_reaction_event(self.message, ARROW_LEFT, self.player.id, self.on_back_reaction)
        await MessageManager.add_reaction_event(self.message, CHECKMARK, self.player.id, self.on_checkmark_reaction)
        await MessageManager.add_reaction_event(self.message, STOP, self.player.id, self.on_stop_reaction)

        self.start_timer()

    async def on_back_reaction(self):
        self.cancel_timer()

        await MessageManager.remove_reaction(self.message, ARROW_LEFT, self.player.member)
        if len(self.code) > 0:
            color = self.code[-1]
            await MessageManager.remove_reaction(self.message, COLORS_EMOJI[color], self.player.member)
            self.code.remove(color)
            await MessageManager.edit_message(self.message, self.get_content())

        self.start_timer()

    async def on_color_reaction(self, color_emoji):
        self.cancel_timer()

        for color, emoji in COLORS_EMOJI.items():
            if emoji == color_emoji and color not in self.code and len(self.code) < 4:
                self.code.append(color)
            elif emoji == color_emoji:
                await MessageManager.remove_reaction(self.message, emoji, self.player.member)
        await MessageManager.edit_message(self.message, self.get_content())

        self.start_timer()

    async def on_checkmark_reaction(self):
        self.cancel_timer()

        await MessageManager.remove_reaction(self.message, CHECKMARK, self.player.member)
        if len(self.code) == 4:
            self.mastermind.guess(self.code)
            for color in self.code:
                await MessageManager.remove_reaction(self.message, COLORS_EMOJI[color], self.player.member)
            self.code = []

        if self.mastermind.has_won():
            self.player.wins += 1
            await self.end_game()
            return
        elif self.mastermind.has_lost():
            self.player.losses += 1
            await self.end_game()
            return

        await MessageManager.edit_message(self.message, self.get_content())

        self.start_timer()

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
        if self.finished:
            if self.mastermind.has_won():
                content += "You have won the game!"
            else:
                content += f"You have lost the game!\nThe code was: "
                for color in self.mastermind.code:
                    content += COLORS_EMOJI[color]
        return content
