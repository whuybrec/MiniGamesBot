from Other.private import Private
from Other.variables import *
from string import ascii_lowercase

class HangMan:
    def __init__(self, gamemanager, msg, playerID):
        self.gamemanager = gamemanager
        self.playerID = playerID
        self.word = getRandomWord()
        self.guessed_word = ["" for i in range(len(self.word))]
        self.index = 1
        self.msg = msg
        self.msg2 = None

    async def start_game(self):
        await self.msg.edit(content=self.get_board())
        self.msg2 = await self.msg.channel.send("** **")
        self.gamemanager.open_games[self.msg2.id] = self
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
            await self.msg.edit(content="Game closed.")
            await self.end_game(self.msg)
            return

        letter = ""
        for letter, emoji in Variables.DICT_ALFABET.items():
            if emoji == reaction.emoji and letter in self.word:
                for i in range(len(self.word)):
                    if self.word[i] == letter:
                        self.guessed_word[i] = letter
                break
        if not letter in self.word:
            self.index+=1

        await self.msg.edit(content=self.get_board())

        if self.index == 10:
            await reaction.message.channel.send("<@" +str(self.playerID) + "> lost the game!")
            await self.end_game(self.msg)
            return

        if "".join(self.guessed_word) == self.word:
            await reaction.message.channel.send("Congratulations <@" +str(self.playerID) + ">, you found the word!")
            await self.end_game(self.msg)

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

    async def end_game(self, message):
        await self.msg2.delete()
        del self.gamemanager.open_games[self.msg2.id]
        await self.gamemanager.close_game(message)

