from discordbot.messagemanager import MessageManager
from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.emojis import ALPHABET, STOP, ARROW_LEFT
from minigames.scramble import Scramble


class ScrambleDiscord(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.scramble_game = Scramble()
        self.player = self.session.players[0]

    async def start_game(self):
        await MessageManager.edit_message(self.message, self.get_content())

        await MessageManager.add_reaction_event(self.message, STOP, self.player.id, self.on_stop_reaction)
        await MessageManager.add_reaction_event(self.message, ARROW_LEFT, self.player.id, self.on_back_reaction)
        for c in self.scramble_game.scrambled_word:
            await MessageManager.add_reaction_event(self.message, ALPHABET[c], self.player.id, self.on_letter_reaction,
                                                    ALPHABET[c])

        self.start_timer()

    async def on_letter_reaction(self, letter_emoji):
        self.cancel_timer()

        for char, emoji in ALPHABET.items():
            if emoji == letter_emoji:
                self.scramble_game.guess(char)
                if char not in self.scramble_game.scrambled_word:
                    await MessageManager.clear_reaction(self.message, letter_emoji)
                else:
                    await MessageManager.remove_reaction(self.message, letter_emoji, self.player.member)
                break

        if self.scramble_game.has_won():
            self.player.wins += 1
            await self.end_game()
            return

        await MessageManager.edit_message(self.message, self.get_content())
        self.start_timer()

    async def on_back_reaction(self):
        self.cancel_timer()

        char = self.scramble_game.remove_last()
        if char != "_":
            await MessageManager.add_reaction_event(self.message, ALPHABET[char], self.player.id,
                                                    self.on_letter_reaction)
        await MessageManager.remove_reaction(self.message, ARROW_LEFT, self.player.member)
        await MessageManager.edit_message(self.message, self.get_content())

        self.start_timer()

    def get_content(self):
        current_word = self.scramble_game.current_word
        scrambled_word = self.scramble_game.scrambled_word
        word_ = ""
        for c in current_word:
            if c == "_":
                word_ += "__ "
            else:
                word_ += f"{c} "

        content = f"```\nLetters: {' '.join(scrambled_word)}\n" \
                  f"{''.join(word_)}\n```"
        if self.finished and self.scramble_game.has_won():
            content += "```\nYou have won the game!\n```"
        elif self.finished:
            content += f"```\nYou have lost the game!\nThe word was: '{''.join(self.scramble_game.word)}'\n```"
        elif len(scrambled_word) == 0:
            content += "```\nWrong word, try again!\n```"
        return content
