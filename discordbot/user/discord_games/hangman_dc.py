from string import ascii_lowercase

from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.emojis import ALPHABET, STOP
from minigames.hangman import Hangman, HANGMEN


class HangmanDisc(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.hangman_game = Hangman()

    async def start(self):
        await self.session.message.edit(content=self.get_content())

        for i in range(len(ascii_lowercase)):
            if i < 13:
                await self.add_reaction(ALPHABET[ascii_lowercase[i]])
            if i >= 13:
                await self.add_reaction(ALPHABET[ascii_lowercase[i]], True)
        await self.add_reaction(STOP, True)

        await self.wait_for_player(self.check)

    def check(self, r, u):
        return r.message.id in [self.session.message.id, self.session.message_extra.id] \
               and r.emoji in self.emojis \
               and u.id == self.players[self.turn].id

    async def on_reaction(self, reaction, user):
        for letter, emoji in ALPHABET.items():
            if emoji == reaction.emoji:
                self.hangman_game.guess(letter)
                break

        if self.hangman_game.has_won():
            self.winners.append(self.players[0])
            self.playing = False
        elif self.hangman_game.has_lost():
            self.losers.append(self.players[0])
            self.playing = False

        await self.session.message.edit(content=self.get_content())

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
        if not self.playing:
            if len(self.winners) == 1:
                content += "```\nYou have won the game!\n```"
            else:
                content += f"```\nYou have lost the game!\nThe word was: '{''.join(self.hangman_game.word)}'\n```"
        return content
