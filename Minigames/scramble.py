from Other.variables import Variables, get_random_word
from Other.private import Private
import random
from Minigames.minigame import MiniGame

class Scramble(MiniGame):
    def __init__(self, game_manager, msg, player_id):
        super().__init__(game_manager, msg)
        self.player_id = player_id
        self.word = None
        self.scrambledLetters = None
        self.guessedWord = None
        self.wordEmojis = []
        self.wrong_word = False
        self.terminated = False

    async def start_game(self):
        self.word = get_random_word()
        self.scrambledLetters = list(self.word)
        random.shuffle(self.scrambledLetters)
        self.guessedWord = [""]*(len(self.word)+1)
        self.wordEmojis = []
        self.wrong_word = False
        self.terminated = False

        text = self.get_board()
        await self.msg.edit(content=text)
        for letter in self.scrambledLetters:
            self.wordEmojis.append(Variables.DICT_ALFABET[letter])
            await self.msg.add_reaction(Variables.DICT_ALFABET[letter])
        await self.msg.add_reaction(Variables.BACK_EMOJI)
        await self.msg.add_reaction(Variables.STOP_EMOJI)

    async def update_game(self, reaction, user):
        if self.terminated or user.id in Private.BOT_ID:
            return
        if reaction.count != 2 or not user.id == self.player_id:
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
            await self.restart()
            return

        if len(''.join(self.guessedWord)) == len(self.word) and ''.join(self.guessedWord) != self.word:
            self.wrong_word = True
        elif len(''.join(self.guessedWord)) != len(self.word):
            self.wrong_word = False

        text = self.get_board()
        await reaction.message.edit(content=text)
        await reaction.message.remove_reaction(reaction.emoji, user)

        if ''.join(self.guessedWord) == self.word:
            await reaction.message.edit(content="Congratulations! <@" + str(self.player_id) +
                                                "> found the scrambled word!\nThe word was \"" + self.word + "\".")
            await self.restart()
            return

    def get_board(self):
        text = "```SCRAMBLE\n"
        text += "Letters left: " +  ' '.join(self.scrambledLetters) + "\n"
        for i in range(len(self.word)):
            if self.guessedWord[i] != "":
                text += str(self.guessedWord[i]) + " "
            else:
                text += "__ "
        if self.wrong_word:
            text += "\nWrong word, try again!"
        text += "\n```"
        return text
