from string import ascii_lowercase

from discordbot.messagemanager import MessageManager
from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.emojis import ALPHABET, STOP
from minigames.hangman import Hangman, HANGMEN


class HangmanDiscord(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.hangman_game = Hangman()
        self.player = self.session.players[0]

    async def start_game(self):
        await self.session.send_extra_message()
        await MessageManager.edit_message(self.message, self.get_content())

        for i in range(len(ascii_lowercase)):
            emoji = ALPHABET[ascii_lowercase[i]]
            if i < 13:
                await MessageManager.add_reaction_event(self.message, emoji, self.player.id, self.on_letter_reaction, emoji)
            if i >= 13:
                await MessageManager.add_reaction_event(self.extra_message, emoji, self.player.id, self.on_letter_reaction, emoji)
        await MessageManager.add_reaction_event(self.extra_message, STOP, self.player.id, self.on_stop_reaction)

        self.start_timer()

    async def on_letter_reaction(self, letter_emoji):
        self.cancel_timer()

        for letter, emoji in ALPHABET.items():
            if emoji == letter_emoji:
                self.hangman_game.guess(letter)
                break

        if self.hangman_game.has_won():
            self.player.wins += 1
            await self.end_game()
            return
        elif self.hangman_game.has_lost():
            self.player.losses += 1
            await self.end_game()
            return

        await MessageManager.edit_message(self.message, self.get_content())

        self.start_timer()

    def get_content(self):
        word = self.hangman_game.current_word
        hangman = HANGMEN[self.hangman_game.lives]
        word_ = ""
        for c in word:
            if c == "_":
                word_ += "__ "
            else:
                word_ += f"{c} "

        content = f"```\n{hangman}\n\nWord: {word_}\n```"
        if self.finished:
            if self.hangman_game.has_won():
                content += "```\nYou have won the game!\n```"
            else:
                content += f"```\nYou have lost the game!\nThe word was: '{''.join(self.hangman_game.word)}'\n```"
        return content
