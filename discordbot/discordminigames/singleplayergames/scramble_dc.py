from discordbot.discordminigames.singleplayergames.singleplayergame import SinglePlayerGame, WON, LOST, QUIT
from discordbot.messagemanager import MessageManager
from discordbot.utils.emojis import ALPHABET, STOP, ARROW_LEFT
from minigames.scramble import Scramble


class ScrambleDiscord(SinglePlayerGame):
    def __init__(self, session):
        super().__init__(session)
        self.scramble_game = Scramble()

    async def start_game(self):
        await MessageManager.edit_message(self.message, self.get_board())

        await MessageManager.add_reaction_and_event(self.message, STOP, self.player.id, self.on_quit_game)
        await MessageManager.add_reaction_and_event(self.message, ARROW_LEFT, self.player.id, self.on_back_reaction)
        for c in self.scramble_game.scrambled_word:
            await MessageManager.add_reaction_and_event(self.message, ALPHABET[c], self.player.id, self.on_letter_reaction,
                                                        ALPHABET[c])

    async def on_letter_reaction(self, letter_emoji):
        self.on_start_move()

        for char, emoji in ALPHABET.items():
            if emoji == letter_emoji:
                self.scramble_game.guess(char)
                if char not in self.scramble_game.scrambled_word:
                    await MessageManager.clear_reaction(self.message, letter_emoji)
                else:
                    await MessageManager.remove_reaction(self.message, letter_emoji, self.player.member)
                break
        await MessageManager.edit_message(self.message, self.get_board())

        if self.scramble_game.has_won():
            await self.game_won()
            return

    async def on_back_reaction(self):
        self.on_start_move()

        char = self.scramble_game.remove_last()
        if char != "_":
            await MessageManager.add_reaction_and_event(self.message, ALPHABET[char], self.player.id,
                                                        self.on_letter_reaction, ALPHABET[char])
        await MessageManager.remove_reaction(self.message, ARROW_LEFT, self.player.member)
        await MessageManager.edit_message(self.message, self.get_board())

    def get_board(self):
        word_ = ""
        for c in self.scramble_game.current_word:
            if c == "_":
                word_ += "__ "
            else:
                word_ += f"{c} "

        content = f"```\nLetters: {' '.join(self.scramble_game.scrambled_word)}\n" \
                  f"{''.join(word_)}\n```"

        if self.game_state == WON:
            content += "```\nYou have won the game!\n```"
        elif self.game_state == LOST or self.game_state == QUIT:
            content += f"```\nYou have lost the game!\nThe word was: '{''.join(self.scramble_game.word)}'\n```"
        elif len(self.scramble_game.scrambled_word) == 0 and not self.scramble_game.has_won():
            content += "```\nWrong word, try again!\n```"
        return content
