from Other.variables import *
from string import ascii_lowercase
from Commands.minigame import MiniGame

class HangMan(MiniGame):
    def __init__(self, game_manager, msg, playerID):
        super().__init__(game_manager, msg)
        self.playerID = playerID
        self.word = get_random_word()
        self.guessed_word = ["" for i in range(len(self.word))]
        self.index = 1
        self.guesses = list()

    async def start_game(self):
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
        if user.id in Private.BOT_ID: return

        if not user.id == self.playerID:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return

        if reaction.emoji == Variables.STOP_EMOJI:
            await self.msg.edit(content="Game closed.\nThe word was \"" + "".join(self.word) + "\"")
            await self.msg2.delete()
            await self.end_game()
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
            await reaction.message.channel.send("<@" +str(self.playerID) + "> lost the game!\nThe word was \"" + "".join(self.word) + "\"")
            await self.msg2.delete()
            await self.end_game()
            return

        if "".join(self.guessed_word) == self.word:
            await reaction.message.channel.send("Congratulations <@" +str(self.playerID) + ">, you found the word!")
            await self.msg2.delete()
            await self.end_game()

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

