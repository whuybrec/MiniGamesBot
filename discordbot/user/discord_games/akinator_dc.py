from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.emojis import ALPHABET, STOP, QUESTION
from akinator.async_aki import Akinator

class AkinatorDisc(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.akinator = Akinator()

    async def start(self):
        await self.akinator.start_game()
        await self.session.message.edit(content=self.get_content())
        await self.add_reaction(ALPHABET["y"])
        await self.add_reaction(ALPHABET["n"])
        await self.add_reaction(QUESTION)
        await self.add_reaction(STOP)

        await self.wait_for_player()

    async def on_reaction(self, reaction, user):
        if reaction.emoji == ALPHABET["y"]:
            await self.akinator.answer(0)
        elif reaction.emoji == ALPHABET["n"]:
            await self.akinator.answer(1)
        else:
            await self.akinator.answer(2)

        await self.session.message.remove_reaction(reaction.emoji, user)

        if self.akinator.progression >= 80:
            await self.akinator.win()
            self.playing = False
        await self.session.message.edit(content=self.get_content())

    def get_content(self):
        content = f"Question {int(self.akinator.step)+1}: *{self.akinator.question}*\n"
        if not self.playing:
            content = f"Akinator guesses: {self.akinator.first_guess['name']}\n{self.akinator.first_guess['absolute_picture_path']}"
        return content
