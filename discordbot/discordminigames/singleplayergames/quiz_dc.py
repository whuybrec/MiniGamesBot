import html
import random
from string import ascii_lowercase, ascii_uppercase

from discordbot.messagemanager import MessageManager
from discordbot.discordminigames.singleplayergames.singleplayergame import SinglePlayerGame, WON, LOST, QUIT
from discordbot.utils.emojis import ALPHABET, STOP, NUMBERS
from minigames.lexicon import Lexicon


class QuizDiscord(SinglePlayerGame):
    def __init__(self, session):
        super().__init__(session)
        self.category = None
        self.question = None
        self.correct_answer = None
        self.answers = None
        self.user_answer = -1
        self.selecting_category = True
        self.categories = ["General Knowledge", "Sports", "Films", "Music", "Video Games"]

    async def start_game(self):
        await MessageManager.edit_message(self.message, self.get_board())

        for i in range(1, len(self.categories) + 1):
            await MessageManager.add_reaction_and_event(self.message, NUMBERS[i], self.player.id, self.choose_category,
                                                        NUMBERS[i])
        await MessageManager.add_reaction_and_event(self.message, STOP, self.player.id, self.on_quit_game)

    async def choose_category(self, emoji):
        self.on_start_move()

        for n, e in NUMBERS.items():
            if e == emoji:
                self.category = self.categories[n - 1]
        self.set_question()
        await MessageManager.edit_message(self.message, self.get_board())

        await self.clear_reactions()
        for i in range(len(self.answers)):
            emoji = ALPHABET[ascii_lowercase[i]]
            await MessageManager.add_reaction_and_event(self.message, emoji, self.player.id, self.choose_answer, emoji)
        await MessageManager.add_reaction_and_event(self.message, STOP, self.player.id, self.on_quit_game)

    async def choose_answer(self, emoji):
        self.on_start_move()

        for c, e in ALPHABET.items():
            if e == emoji:
                self.user_answer = ascii_lowercase.index(c)
                if self.user_answer == self.correct_answer:
                    await self.game_won()
                else:
                    await self.game_lost()
                break

    def set_question(self):
        self.selecting_category = False
        questions = Lexicon.QUESTIONS[self.category]
        random.shuffle(questions)
        quiz = questions[random.randint(0, len(Lexicon.QUESTIONS) - 1)]
        self.question = quiz['question']
        self.answers = list(set(quiz['incorrect_answers']))
        self.correct_answer = random.randint(0, len(self.answers))
        self.answers.insert(self.correct_answer, quiz['correct_answer'])

    async def on_quit_game(self):
        if self.selecting_category:
            self.game_state = -1
        else:
            self.game_state = QUIT
        await self.end_game()

    def get_board(self):
        content = ""
        if self.selecting_category:
            content += "**Categories**\n"
            for i in range(len(self.categories)):
                content += f"{NUMBERS[i + 1]}   *{self.categories[i]}*\n"
            return content

        content += f"**{self.category}**\n\n" \
                   f"*{html.unescape(self.question)}*\n\n"
        for i in range(len(self.answers)):
            if i == self.user_answer:
                content += f"__{ascii_uppercase[i]}) {html.unescape(self.answers[i])}__\n"
            else:
                content += f"{ascii_uppercase[i]}) {html.unescape(self.answers[i])}\n"

        if self.game_state == WON:
            content += "\nYou answered correct!"
        elif self.game_state == LOST or self.game_state == QUIT:
            content += f"\nWrong! The correct answer was: {html.unescape(self.answers[self.correct_answer])}"
        return content
