from Other.private import Private
from Other.variables import Variables, increment_game
import random
import html

class QuizMaster:
    def __init__(self, gamemanager, msg, playerID):
        self.gamemanager = gamemanager
        self.msg = msg
        self.playerID = playerID
        self.count_right = 0
        self.count_wrong = 0
        self.answers = []
        self.possabilities = {Variables.DICT_ALFABET['a']: 0, Variables.DICT_ALFABET['b']: 0, Variables.DICT_ALFABET['c']: 0, Variables.DICT_ALFABET['d']: 0}
        self.question = None
        self.category = None

    async def start_game(self):
        text =  "```\n"
        text += "Categories:\n"
        for i in range(len(Variables.quiz_categories)):
            text += "{0}\t{1}\n".format(Variables.NUMBERS[i+1], Variables.quiz_categories[i])
            await self.msg.add_reaction(Variables.NUMBERS[i+1])
        text += "\n```"
        await self.msg.edit(content=text)
        await self.msg.add_reaction(Variables.STOP_EMOJI)

    async def start_quiz(self):
        questions = Variables.questions_dict[self.category]
        random.shuffle(questions)
        self.question = questions[random.randint(0, len(Variables.questions_dict)-1)]
        self.answers =  self.question['incorrect_answers']
        self.answers.append(self.question['correct_answer'])
        random.shuffle(self.answers)

        count = 0
        for key in self.possabilities.keys():
            self.possabilities[key] = html.unescape(self.answers[count])
            count += 1

        await self.msg.edit(content=self.get_board())
        await self.msg.add_reaction(Variables.DICT_ALFABET['a'])
        await self.msg.add_reaction(Variables.DICT_ALFABET['b'])
        await self.msg.add_reaction(Variables.DICT_ALFABET['c'])
        await self.msg.add_reaction(Variables.DICT_ALFABET['d'])
        await self.msg.add_reaction(Variables.STOP_EMOJI)

    async def end_game(self, message):
        await self.gamemanager.close_game(message)

    async def update_game(self, reaction, user):
        if user.id in Private.BOT_ID: return
        if not user.id == self.playerID:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return

        if reaction.emoji == Variables.STOP_EMOJI:
            await self.end_game(self.msg)
            await self.msg.edit(content="Game closed.")
            return

        if reaction.emoji in Variables.NUMBERS:
            index = Variables.NUMBERS.index(reaction.emoji) - 1
            self.category = Variables.quiz_categories[index]
            await self.msg.clear_reactions()
            await self.start_quiz()
            return

        if reaction.emoji in self.possabilities.keys():
            if self.possabilities[reaction.emoji] == html.unescape(self.question['correct_answer']):
                self.count_right += 1
            else:
                self.count_wrong += 1
            await self.msg.edit(content=self.get_board())
            await self.msg.clear_reactions()
            await self.msg.add_reaction(Variables.NEXT_EMOJI)
            await self.msg.add_reaction(Variables.STOP_EMOJI)
            return

        if reaction.emoji == Variables.NEXT_EMOJI:
            await self.msg.clear_reactions()
            increment_game("quiz")
            await self.start_quiz()
            return

    def get_board(self):
        text = "```\n" \
               "{0}\n" \
               "Question:\n{1}\n\n" \
               "A: {2}\n" \
               "B: {3}\n" \
               "C: {4}\n" \
               "D: {5}\n\n" \
               "Correct answers: {6}\n" \
               "Incorrect answers: {7}\n" \
               "```".format(self.question['category'], html.unescape(self.question['question']),
                            self.possabilities[Variables.DICT_ALFABET['a']],
                            self.possabilities[Variables.DICT_ALFABET['b']],
                            self.possabilities[Variables.DICT_ALFABET['c']],
                            self.possabilities[Variables.DICT_ALFABET['d']],
                            self.count_right, self.count_wrong)
        return text
