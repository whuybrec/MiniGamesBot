import asyncio
import html
import random
from string import ascii_lowercase, ascii_uppercase

from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.user.variables import TIMEOUT, WIN, LOSE
from discordbot.utils.emojis import ALPHABET, STOP, NUMBERS
from minigames.lexicon import Lexicon


class QuizDisc(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.category = None
        self.question = None
        self.correct_answer = None
        self.answers = None
        self.user_answer = -1
        self.selecting_category = True
        self.categories = ["General Knowledge", "Sports", "Films", "Music", "Video Games"]

    async def start(self):
        if self.session.message_extra is not None:
            await self.session.message_extra.delete()
            self.session.message_extra = None

        await self.session.message.edit(content=self.get_content())

        for i in range(1, len(self.categories)+1):
            await self.session.message.add_reaction(NUMBERS[i])
            self.emojis.add(NUMBERS[i])
        await self.session.message.add_reaction(STOP)
        self.emojis.add(STOP)

        def check(r, u):
            return r.message.id == self.session.message.id \
                   and u.id != self.session.message.author.id \
                   and r.emoji in self.emojis \
                   and u.id == self.session.context.author.id

        try:
            reaction, user = await self.session.bot.wait_for("reaction_add", check=check, timeout=TIMEOUT)
            if self.has_pressed_stop(reaction):
                self.status = LOSE
                await self.end_game()
                return
            else:
                for n, e in NUMBERS.items():
                    if e == reaction.emoji:
                        self.category = self.categories[n-1]
                        break
        except asyncio.TimeoutError:
            await self.end_game()
            return

        await self.session.message.clear_reactions()
        self.emojis = set()

        self.selecting_category = False
        questions = Lexicon.QUESTIONS[self.category]
        random.shuffle(questions)
        quiz = questions[random.randint(0, len(Lexicon.QUESTIONS) - 1)]
        self.question = quiz['question']
        self.answers = list(set(quiz['incorrect_answers']))
        self.correct_answer = random.randint(0, len(self.answers))
        self.answers.insert(self.correct_answer, quiz['correct_answer'])

        await self.session.message.edit(content=self.get_content())
        for i in range(len(self.answers)):
            await self.session.message.add_reaction(ALPHABET[ascii_lowercase[i]])
            self.emojis.add(ALPHABET[ascii_lowercase[i]])
        await self.session.message.add_reaction(STOP)
        self.emojis.add(STOP)

        await self.wait_for_player()

    async def wait_for_player(self):
        while True:
            def check(r, u):
                return r.message.id == self.session.message.id \
                       and u.id != self.session.message.author.id

            try:
                reaction, user = await self.session.bot.wait_for("reaction_add", check=check, timeout=TIMEOUT)
                if await self.validate(reaction, user):
                    if self.has_pressed_stop(reaction):
                        self.status = LOSE
                        break

                    for c, e in ALPHABET.items():
                        if e == reaction.emoji:
                            self.user_answer = ascii_lowercase.index(c)
                            if self.user_answer == self.correct_answer:
                                self.status = WIN
                            else:
                                self.status = LOSE
                            break
                    break
            except asyncio.TimeoutError:
                self.status = LOSE

        await self.session.message.edit(content=self.get_content())
        await self.end_game()

    def get_content(self):
        content = "```"
        if self.selecting_category:
            content += "Categories\n"
            for i in range(len(self.categories)):
                content += f"{NUMBERS[i+1]}   {self.categories[i]}\n"
        else:
            content += f"{self.category}\nQuestion:\n" \
                       f"{html.unescape(self.question)}\n\n"
            for i in range(len(self.answers)):
                if i == self.user_answer:
                    content += f"{ascii_uppercase[i]}: {html.unescape(self.answers[i])}   <- YOUR ANSWER\n"
                else:
                    content += f"{ascii_uppercase[i]}: {html.unescape(self.answers[i])}\n"
            if self.status == WIN:
                content += "You answered correct!\n"
            elif self.status == LOSE:
                content += f"Wrong! The correct answer was: {html.unescape(self.answers[self.correct_answer])}\n"
        content += "```"
        return content
