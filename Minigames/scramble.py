from Other.variables import Variables, getRandomWord
from Other.private import Private
import random

class Scramble:
    def __init__(self, gamemanager, msg, playerID):
        self.gamemanager = gamemanager
        self.msg = msg
        self.playerID = playerID
        self.word = getRandomWord()
        self.scrambledLetters = list(self.word)
        random.shuffle(self.scrambledLetters)
        self.guessedWord = [""]*(len(self.word)+1)
        self.wordEmojis = []

    async def start_game(self):
        text = self.getBoard()
        await self.msg.edit(content=text)
        for letter in self.scrambledLetters:
            self.wordEmojis.append(Variables.DICT_ALFABET[letter])
            await self.msg.add_reaction(Variables.DICT_ALFABET[letter])
        await self.msg.add_reaction(Variables.BACK_EMOJI)
        await self.msg.add_reaction(Variables.STOP_EMOJI)

    async def update_game(self, reaction, user):
        if user.id in Private.BOT_ID: return

        if not user.id == self.playerID:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return

        if reaction.emoji in self.wordEmojis:
            for i in range(len(self.guessedWord)):
                if self.guessedWord[i] == "":
                    for key, value in Variables.DICT_ALFABET.items():
                        if value == reaction.emoji:
                            if key in self.scrambledLetters:
                                self.guessedWord[i] = key
                                self.scrambledLetters.remove(key)
                            break
                    break
        elif reaction.emoji == Variables.BACK_EMOJI:
            for i in range(len(self.guessedWord)):
                if self.guessedWord[i] == "":
                    self.scrambledLetters.append(self.guessedWord[i-1])
                    self.guessedWord[i-1] = ""
                    break
        elif reaction.emoji == Variables.STOP_EMOJI:
            await self.msg.edit(content="Game closed.\nThe word was \"" + "".join(self.word) + "\"")
            await self.gamemanager.close_game(self.msg)
            return

        text = self.getBoard()
        await reaction.message.remove_reaction(reaction.emoji, user)
        await reaction.message.edit(content=text)

        if ''.join(self.guessedWord) == self.word:
            await reaction.message.channel.send("Congratulations! <@" + str(self.playerID) + "> found the scrambled word!")
            await self.gamemanager.close_game(self.msg)

    def getBoard(self):
        text  = "```SCRAMBLE\n"
        text += "Letters left: " +  ' '.join(self.scrambledLetters) +"\n"
        for i in range(len(self.word)):
            if self.guessedWord[i] != "":
                text += str(self.guessedWord[i]) + " "
            else:
                text += "__ "
        text += "\n```"
        return text

