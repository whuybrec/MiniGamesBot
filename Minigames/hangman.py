from Other.variables import *
from string import ascii_lowercase
from Minigames.minigame import MiniGame

class HangMan(MiniGame):
    def __init__(self, game_manager, msg, player_id):
        super().__init__(game_manager, msg)
        self.player_id = player_id
        self.word = get_random_word()
        self.guessed_word = None
        self.index = None
        self.guesses = list()
        self.terminated = False

    async def start_game(self):
        self.terminated = False
        self.word = get_random_word()
        self.guessed_word = ["" for i in range(len(self.word))]
        self.index = 1
        self.guesses = list()

        await self.msg.edit(content=self.get_board())
        self.msg2 = await self.msg.channel.send("** **")
        self.game_manager.open_games[self.msg2.id] = self
        for i in range(len(ascii_lowercase)):
            if i < 13:
                await self.msg.add_reaction(Variables.DICT_ALFABET[ascii_lowercase[i]])
            if i >= 13:
                await self.msg2.add_reaction(Variables.DICT_ALFABET[ascii_lowercase[i]])
        await self.msg2.add_reaction(Variables.STOP_EMOJI)

    async def update_game(self, reaction, user):
        if self.terminated:
            return
        if user.id in Private.BOT_ID:
            return
        if reaction.count != 2:
            return
        if not user.id == self.player_id:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return

        if reaction.emoji == Variables.STOP_EMOJI:
            await self.msg2.delete()
            await self.msg.edit(content="Game closed.\nThe word was \"" + "".join(self.word) + "\"")
            await self.restart()
            return

        letter = ""
        for letter, emoji in Variables.DICT_ALFABET.items():
            if emoji == reaction.emoji:
                break

        if letter in self.word:
            self.guesses.append(letter)
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    self.guessed_word[i] = letter

        else:
            if not letter in self.guesses:
                self.guesses.append(letter)
                self.index += 1

        await self.msg.edit(content=self.get_board())

        if self.index == 10:
            await self.msg2.delete()
            await self.msg.edit(content=self.get_board() + "\n<@" + str(self.player_id) + "> lost the game!"
                                        "\nThe word was \"" + "".join(self.word) + "\"")
            await self.restart()
            return

        if "".join(self.guessed_word) == self.word:
            await self.msg2.delete()
            await self.msg.edit(content=self.get_board() + "\nCongratulations <@" + str(self.player_id) +
                                        ">, you found the word!")
            await self.restart()

    def get_word_status(self):
        text = ""
        for char in self.guessed_word:
            if char == "":
                text += "__ "
            else:
                text += char + " "
        return text

    def get_board(self):
        text = "```\n"
        text += Variables.hangmen[self.index]
        text += "\n\nWord: " + self.get_word_status()
        text += "\n```"
        return text
