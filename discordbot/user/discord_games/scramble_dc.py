from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.emojis import ALPHABET, STOP, ARROW_LEFT_2
from minigames.scramble import Scramble


class ScrambleDisc(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.scramble_game = Scramble()

    async def start(self):
        await self.session.message.edit(content=self.get_content())
        await self.add_reaction(STOP)
        await self.add_reaction(ARROW_LEFT_2)
        for c in self.scramble_game.scrambled_word:
            await self.add_reaction(ALPHABET[c])

        await self.wait_for_player()

    async def on_reaction(self, reaction, user):
        if reaction.emoji == ARROW_LEFT_2:
            char = self.scramble_game.remove_last()
            if char != "_":
                await self.add_reaction(ALPHABET[char])
            await self.session.message.remove_reaction(reaction.emoji, user)
        else:
            for c, e in ALPHABET.items():
                if e == reaction.emoji:
                    self.scramble_game.guess(c)
                    if c not in self.scramble_game.scrambled_word:
                        await self.clear_reaction(e)
                    else:
                        await self.session.message.remove_reaction(e, user)
                    break

        if self.scramble_game.has_won():
            self.winners.append(self.players[0])
            self.playing = False
        await self.session.message.edit(content=self.get_content())

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
        if not self.playing:
            if len(self.winners) == 1:
                content += "```\nYou have won the game!\n```"
            else:
                content += f"```\nYou have lost the game!\nThe word was: '{''.join(self.scramble_game.word)}'\n```"
        elif len(scrambled_word) == 0:
            content += "```\nWrong word, try again!\n```"
        return content
