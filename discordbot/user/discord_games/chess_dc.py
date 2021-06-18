import random
from string import ascii_lowercase

import chess
import discord
from chess import Board, svg

from discordbot.messagemanager import MessageManager
from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.emojis import ALPHABET, STOP, NUMBERS, ARROW_LEFT
from discordbot.utils.private import DISCORD


# TURN: 0 WHITE
# TURN: 1 BLACK


class ChessDiscord(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.chessboard = Board()
        self.turn = random.randint(0, 1)
        self.move = ""
        self.choosing_letter = True
        self.choosing_number = False
        self.id = random.getrandbits(64)
        self.file = f'bin/{self.id}'

    async def start_game(self):
        await self.update_messages()

        for i in range(8):
            emoji = ALPHABET[ascii_lowercase[i]]
            await MessageManager.add_reaction_event(self.message, emoji, self.players[self.turn].id,
                                                    self.on_letter_reaction, emoji)
        for i in range(1, 9):
            emoji = NUMBERS[i]
            await MessageManager.add_reaction_event(self.extra_message, emoji, self.players[self.turn].id,
                                                    self.on_number_reaction, emoji)

        await MessageManager.add_reaction_event(self.extra_message, ARROW_LEFT, self.players[self.turn].id,
                                                self.on_back_reaction)
        await MessageManager.add_reaction_event(self.extra_message, STOP, self.players[0].id, self.on_stop_reaction)
        await MessageManager.add_reaction_event(self.extra_message, STOP, self.players[1].id, self.on_stop_reaction)

        self.start_timer()

    async def on_letter_reaction(self, letter_emoji):
        self.cancel_timer()

        if self.choosing_letter:
            for char, emoji in ALPHABET.items():
                if letter_emoji == emoji:
                    self.move += char
            self.choosing_number = True
            self.choosing_letter = False
            await MessageManager.edit_message(self.message, self.get_content())
        await MessageManager.remove_reaction(self.message, letter_emoji, self.players[self.turn].member)

        self.start_timer()

    async def on_number_reaction(self, number_emoji):
        self.cancel_timer()

        if self.choosing_number:
            for n, emoji in NUMBERS.items():
                if number_emoji == emoji:
                    self.move += str(n)
            self.choosing_number = False
            self.choosing_letter = True
            await MessageManager.edit_message(self.message, self.get_content())
        await MessageManager.remove_reaction(self.extra_message, number_emoji, self.players[self.turn].member)
        await self.check_end_move()

        self.start_timer()

    async def on_back_reaction(self):
        self.session.set_stopwatch()

        if len(self.move) > 0:
            self.move = self.move[:-1]
            self.choosing_number = not self.choosing_number
            self.choosing_letter = not self.choosing_letter
            await MessageManager.edit_message(self.message, self.get_content())
        await MessageManager.remove_reaction(self.extra_message, ARROW_LEFT, self.players[self.turn].member)

    async def check_end_move(self):
        if len(self.move) == 4:
            try:
                if chess.Move.from_uci(self.move) in self.chessboard.legal_moves:
                    self.chessboard.push_uci(self.move)
                    self.move = ""

                    if self.chessboard.is_checkmate():
                        self.players[self.turn].wins += 1
                        self.players[(self.turn + 1) % 2].losses += 1
                        await self.end_game()
                        return

                    elif self.chessboard.is_stalemate() or self.chessboard.is_insufficient_material():
                        self.players[self.turn].draws += 1
                        self.players[(self.turn + 1) % 2].draws += 1
                        await self.end_game()
                        return

                    old_turn = self.turn
                    self.turn = (self.turn + 1) % 2
                    await self.update_messages()

                    for i in range(8):
                        emoji = ALPHABET[ascii_lowercase[i]]
                        await MessageManager.add_reaction_event(self.message, emoji, self.players[self.turn].id,
                                                                self.on_letter_reaction, emoji)
                        await MessageManager.remove_reaction_event(self.message.id, emoji, self.players[old_turn].id)
                    for i in range(1, 9):
                        emoji = NUMBERS[i]
                        await MessageManager.add_reaction_event(self.extra_message, emoji, self.players[self.turn].id,
                                                                self.on_number_reaction, emoji)
                        await MessageManager.remove_reaction_event(self.extra_message.id, emoji,
                                                                   self.players[old_turn].id)
                    return
            except ValueError:
                pass
            self.move = ""
            await MessageManager.edit_message(self.message, self.get_content() + "\nIncorrect move, try again!")

    async def end_game(self):
        self.remove_files()
        await super().end_game()

    async def on_stop_reaction(self):
        self.cancel_timer()
        self.players[self.turn].losses += 1
        self.players[(self.turn + 1) % 2].wins += 1
        await self.end_game()

    async def on_player_timed_out(self):
        self.players[self.turn].unfinished += 1
        self.players[self.turn].losses += 1
        self.players[(self.turn + 1) % 2].wins += 1
        await self.end_game()

    async def update_messages(self):
        self.save_board_image()

        dump_channel = await self.session.game_manager.bot.fetch_channel(DISCORD['STACK_CHANNEL'])
        msg_dump = await dump_channel.send(file=discord.File(self.file + ".png"))
        await self.session.send_extra_message()
        await MessageManager.edit_message(self.message, self.get_content())
        await MessageManager.edit_message(self.extra_message, msg_dump.attachments[0].url)

    def get_content(self):
        if self.finished:
            if self.chessboard.is_checkmate():
                content = f"<@{str(self.players[self.turn].id)}> won the game!"
            else:
                content = f"Game ended in draw!"
        else:
            if self.turn == 0:
                color = "White"
            else:
                color = "Black"
            content = f"{color}'s turn: <@{str(self.players[self.turn].id)}>\n"
            if self.choosing_number:
                content += "\nSelect **number**"
            if self.choosing_letter:
                content += "\nSelect **letter**"
            if self.chessboard.is_check():
                content += "\n**CHECK**"
            content += "\nMove: "
            if self.move != "":
                content += f"**{self.move}**"
        return content

    def save_board_image(self):
        try:
            move = self.chessboard.peek()
            drawing = svg.board(self.chessboard, size=250, lastmove=move)
        except IndexError:
            drawing = svg.board(self.chessboard, size=250)
        f = open(f'{self.file}.svg', 'w')
        f.write(drawing)
        import os
        os.system(f'svgexport {self.file}.svg {self.file}.png 1.5x')

    def remove_files(self):
        import os
        os.remove(f"{self.file}.svg")
        os.remove(f"{self.file}.png")
