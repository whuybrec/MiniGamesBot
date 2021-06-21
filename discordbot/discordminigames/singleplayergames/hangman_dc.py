from string import ascii_lowercase

from discordbot.messagemanager import MessageManager
from discordbot.discordminigames.singleplayergames.singleplayergame import SinglePlayerGame, WON, LOST, QUIT
from discordbot.utils.emojis import ALPHABET, STOP
from minigames.hangman import Hangman, HANGMEN


class HangmanDiscord(SinglePlayerGame):
    def __init__(self, session):
        super().__init__(session)
        self.hangman_game = Hangman()

    async def start_game(self):
        await self.session.send_extra_message()
        await MessageManager.edit_message(self.message, self.get_board())

        for i in range(len(ascii_lowercase)):
            emoji = ALPHABET[ascii_lowercase[i]]
            if i < 13:
                await MessageManager.add_reaction_and_event(self.message, emoji, self.player.id, self.on_letter_reaction,
                                                            emoji)
            if i >= 13:
                await MessageManager.add_reaction_and_event(self.extra_message, emoji, self.player.id,
                                                            self.on_letter_reaction, emoji)
        await MessageManager.add_reaction_and_event(self.extra_message, STOP, self.player.id, self.on_quit_game)

    async def on_letter_reaction(self, letter_emoji):
        self.on_start_move()

        for letter, emoji in ALPHABET.items():
            if emoji == letter_emoji:
                self.hangman_game.guess(letter)
                break

        if self.hangman_game.has_won():
            await self.game_won()
            return
        elif self.hangman_game.has_lost():
            await self.game_lost()
            return

        await MessageManager.edit_message(self.message, self.get_board())

    def get_board(self):
        word = self.hangman_game.current_word
        hangman = HANGMEN[self.hangman_game.lives]
        word_ = ""
        for c in word:
            if c == "_":
                word_ += "__ "
            else:
                word_ += f"{c} "

        content = f"```\n{hangman}\n\nWord: {word_}\n```"
        if self.game_state == WON:
            content += "```\nYou have won the game!\n```"
        elif self.game_state == LOST or self.game_state == QUIT:
            content += f"```\nYou have lost the game!\nThe word was: '{''.join(self.hangman_game.word)}'\n```"
        return content
