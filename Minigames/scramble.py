from Other.variables import Variables, get_random_word
import random
import asyncio
from Minigames.minigame import MiniGame

class Scramble(MiniGame):
    def __init__(self, bot, game_name, msg, player_id):
        super().__init__(bot, game_name, msg, player_id)
        self.word = None
        self.scrambledLetters = None
        self.guessedWord = None
        self.wordEmojis = []
        self.wrong_word = False
        self.terminated = False

    async def start_game(self):
        self.init_var()

        text = self.get_board()
        await self.msg.edit(content=text)
        for letter in self.scrambledLetters:
            self.wordEmojis.append(Variables.DICT_ALFABET[letter])
            await self.msg.add_reaction(Variables.DICT_ALFABET[letter])
        await self.msg.add_reaction(Variables.BACK_EMOJI)
        await self.msg.add_reaction(Variables.STOP_EMOJI)

        await self.wait_for_player()

    async def update_game(self, reaction, user):
        if self.terminated:
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
            self.losses += 1
            await reaction.message.edit(content="Game closed.\n"
                                                "The word was \"{0}\".\n"
                                                "```Wins: {1}\nLosses: {2}\n```".format(self.word,
                                                                                         self.wins,
                                                                                         self.losses))
            await self.msg.clear_reactions()
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
            self.wins += 1
            await reaction.message.edit(content="Congratulations! <@{0}> found the scrambled word!\n"
                                                "The word was \"{1}\".\n"
                                                "```Wins: {2}\nLosses: {3}\n```".format(self.player_id, self.word,
                                                                                         self.wins,
                                                                                         self.losses))
            await self.restart()
            return

        await self.wait_for_player()

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
        text += "``````Wins: {0}\nLosses: {1}\n```".format(self.wins, self.losses)
        return text

    def init_var(self):
        self.word = get_random_word()
        self.scrambledLetters = list(self.word)
        random.shuffle(self.scrambledLetters)
        self.guessedWord = [""] * (len(self.word) + 1)
        self.wordEmojis = []
        self.wrong_word = False
        self.terminated = False
