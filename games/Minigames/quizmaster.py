from discordbot.variables import Variables
from string import ascii_lowercase
import random
import html
from games.Minigames.minigame import MiniGame


class QuizMaster(MiniGame):
    def __init__(self, bot, game_name, msg, player_id):
        super().__init__(bot, game_name, msg, player_id)
        self.answers = set()
        self.possabilities = dict()
        self.question = None
        self.category = None

    async def start_game(self):
        text = "```\n"
        text += "Categories:\n"
        for i in range(len(Variables.quiz_categories)):
            await self.msg.add_reaction(Variables.NUMBERS[i+1])
            text += "{0}\t{1}\n".format(Variables.NUMBERS[i+1], Variables.quiz_categories[i])
        text += "\n```"
        await self.msg.edit(content=text)
        await self.msg.add_reaction(Variables.STOP_EMOJI)

        await self.wait_for_player()

    async def start_quiz(self):
        self.init_var()

        i = 0
        for answer in self.answers:
            self.possabilities[Variables.DICT_ALFABET[ascii_lowercase[i]]] = html.unescape(answer)
            i += 1
        await self.msg.edit(content=self.get_board())
        for i in range(len(self.answers)):
            await self.msg.add_reaction(Variables.DICT_ALFABET[ascii_lowercase[i]])
        await self.msg.add_reaction(Variables.STOP_EMOJI)

        await self.wait_for_player()

    async def update_game(self, reaction, user):
        if self.terminated:
            return

        if reaction.emoji == Variables.STOP_EMOJI:
            await reaction.message.edit(content="Game closed.\n```Wins: {0}\nLosses: {1}\n```".format(self.wins,
                                                                                                       self.losses))
            await self.restart()
            return

        if reaction.emoji in Variables.NUMBERS:
            index = Variables.NUMBERS.index(reaction.emoji) - 1
            self.category = Variables.quiz_categories[index]
            await self.msg.clear_reactions()
            await self.start_quiz()
            return

        if reaction.emoji in self.possabilities.keys():
            if self.possabilities[reaction.emoji] == html.unescape(self.question['correct_answer']):
                self.wins += 1
            else:
                self.losses += 1
            await self.msg.edit(content=self.get_board(self.possabilities[reaction.emoji], html.unescape(self.question['correct_answer'])))
            await self.msg.clear_reactions()
            await self.restart()
            return

    def get_board(self, u_answer=None, correct_answer=None):
        text = "```\n" \
               "{0}\n" \
               "Question:\n{1}\n".format(self.question['category'], html.unescape(self.question['question']))
        for i in range(len(self.possabilities.keys())):
            text += "\n{0}: {1}".format(ascii_lowercase[i].upper(), self.possabilities[Variables.DICT_ALFABET[ascii_lowercase[i]]])
            if u_answer is not None and self.possabilities[Variables.DICT_ALFABET[ascii_lowercase[i]]] == u_answer:
                text += "  <- YOUR ANSWER"
        text += "\n\nCorrect answers: {0}\n" \
                "Incorrect answers: {1}\n\n".format(self.wins, self.losses)
        if u_answer is not None and correct_answer is not None:
            if u_answer != correct_answer:
                text += "Wrong! The correct answer was: {0}\n".format(correct_answer)
            else:
                text += "Nice! You answered correct!\n"
        text += "```"
        return text

    def init_var(self):
        questions = Variables.questions_dict[self.category]
        random.shuffle(questions)
        self.question = questions[random.randint(0, len(Variables.questions_dict) - 1)]
        self.answers = set(self.question['incorrect_answers'])
        self.answers.add(self.question['correct_answer'])
        random.shuffle(list(self.answers))
