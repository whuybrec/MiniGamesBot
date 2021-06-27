import json.decoder

import akinator.exceptions
from akinator.async_aki import Akinator

from discordbot.discordminigames.singleplayergames.singleplayergame import SinglePlayerGame, UNFINISHED
from discordbot.managers.messagemanager import MessageManager
from discordbot.utils.emojis import ALPHABET, STOP, QUESTION


class AkinatorDiscord(SinglePlayerGame):
    def __init__(self, session):
        super().__init__(session)
        self.akinator = Akinator()
        self.guessed = False

    async def start_game(self):
        await self.akinator.start_game()
        await MessageManager.edit_message(self.message, self.get_board())

        await MessageManager.add_reaction_and_event(self.message, ALPHABET["y"], self.player.id, self.on_yes_reaction)
        await MessageManager.add_reaction_and_event(self.message, ALPHABET["n"], self.player.id, self.on_no_reaction)
        await MessageManager.add_reaction_and_event(self.message, QUESTION, self.player.id, self.on_dontknow_reaction)
        await MessageManager.add_reaction_and_event(self.message, STOP, self.player.id, self.on_quit_game)

    async def on_yes_reaction(self):
        self.on_start_move()
        await MessageManager.remove_reaction(self.message, ALPHABET["y"], self.player.member)
        await self.answer(0)

    async def on_no_reaction(self):
        self.on_start_move()
        await MessageManager.remove_reaction(self.message, ALPHABET["n"], self.player.member)
        await self.answer(1)

    async def on_dontknow_reaction(self):
        self.on_start_move()
        await MessageManager.remove_reaction(self.message, QUESTION, self.player.member)
        await self.answer(2)

    async def answer(self, answer):
        try:
            await self.akinator.answer(answer)
            await MessageManager.edit_message(self.session.message, self.get_board())
            if self.akinator.progression >= 80 or self.akinator.step == 79:
                await self.akinator.win()
                self.guessed = True
                self.game_state = -1
                await self.end_game()
        except (akinator.exceptions.AkiTimedOut, json.decoder.JSONDecodeError):
            self.game_state = -1
            await self.end_game()

    def get_board(self):
        content = f"Question {int(self.akinator.step) + 1}: *{self.akinator.question}*\n"
        if self.guessed:
            content = f"Akinator guesses: {self.akinator.first_guess['name']}\n{self.akinator.first_guess['absolute_picture_path']}"
        return content

    async def on_quit_game(self):
        self.game_state = UNFINISHED
        await self.end_game()
