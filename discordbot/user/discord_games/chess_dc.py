import asyncio
import random
from string import ascii_lowercase

import chess
import discord
from discordbot.utils.private import DISCORD
from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.variables import TIMEOUT, LOSE, DRAW
from discordbot.utils.emojis import ALPHABET, STOP, NUMBERS, ARROW_LEFT_2
from chess import Board, svg

# TURN: 0 WHITE
# TURN: 1 BLACK


class ChessDisc(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.chessboard = Board()
        self.turn = random.randint(0, 1)
        self.move = ""
        self.choosing_letter = True
        self.choosing_number = False
        self.id = random.getrandbits(64)
        self.file = f'bin/{self.id}'

    async def start(self):
        await self.update_messages()

        for i in range(8):
            await self.add_reaction(ALPHABET[ascii_lowercase[i]])
        for i in range(1, 9):
            await self.add_reaction(NUMBERS[i], True)

        await self.add_reaction(ARROW_LEFT_2, True)
        await self.add_reaction(STOP, True)

        await self.wait_for_player(self.check)

    def check(self, r, u):
        return r.message.id in [self.session.message.id, self.session.message_extra.id] \
               and r.emoji in self.emojis \
               and u.id == self.players[self.turn].id

    async def wait_for_player(self, check_=None):
        while self.playing:
            try:
                reaction, user = await self.session.bot.wait_for("reaction_add", check=check_, timeout=TIMEOUT)
                if reaction.emoji == STOP:
                    self.losers.append(self.players[self.turn])
                    self.winners.append(self.players[(self.turn+1) % 2])
                    self.playing = False

                await self.on_reaction(reaction, user)

            except asyncio.TimeoutError:
                self.losers.append(self.players[self.turn])
                self.winners.append(self.players[(self.turn + 1) % 2])
                self.playing = False
                self.session.player_timed_out = self.players[self.turn].id

        await self.end_game()

    async def on_reaction(self, reaction, user):
        if reaction.emoji == ARROW_LEFT_2:
            if len(self.move) > 0:
                self.move = self.move[:-1]
                self.choosing_number = not self.choosing_number
                self.choosing_letter = not self.choosing_letter
                await self.session.message.edit(content=self.get_content())
            await reaction.message.remove_reaction(reaction.emoji, user)

        elif reaction.message.id == self.session.message.id and self.choosing_letter:
            for char, emoji in ALPHABET.items():
                if reaction.emoji == emoji:
                    self.move += char
            self.choosing_number = True
            self.choosing_letter = False
            await self.session.message.edit(content=self.get_content())
            await self.session.message.remove_reaction(reaction.emoji, user)

        elif reaction.message.id == self.session.message_extra.id and self.choosing_number:
            for n, emoji in NUMBERS.items():
                if reaction.emoji == emoji:
                    self.move += str(n)
            self.choosing_number = False
            self.choosing_letter = True
            await self.session.message.edit(content=self.get_content())
            await self.session.message_extra.remove_reaction(reaction.emoji, user)
        else:
            await reaction.message.remove_reaction(reaction.emoji, user)

        if len(self.move) == 4:
            if chess.Move.from_uci(self.move) in self.chessboard.legal_moves:
                self.chessboard.push_uci(self.move)
                self.move = ""
                if self.chessboard.is_checkmate():
                    self.winners.append(self.players[self.turn])
                    self.losers.append(self.players[(self.turn + 1) % 2])
                    self.playing = False
                elif self.chessboard.is_stalemate() or self.chessboard.is_insufficient_material():
                    self.drawers.append(self.players[self.turn])
                    self.drawers.append(self.players[(self.turn + 1) % 2])
                    self.playing = False
                else:
                    self.turn = (self.turn + 1) % 2
                await self.update_messages()
            else:
                self.move = ""
                await self.session.message.edit(content=self.get_content()+"\nIncorrect move, try again!")

    def get_content(self):
        if not self.playing:
            if len(self.drawers) == 2:
                content = f"Game ended in draw!"
            else:
                content = f"<@{str(self.winners[0].id)}> won the game!"
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

    async def update_messages(self):
        self.save_board_image()

        dump_channel = await self.session.bot.fetch_channel(DISCORD['STACK_CHANNEL'])
        msg_dump = await dump_channel.send(file=discord.File(self.file + ".png"))
        await self.session.message.edit(content=self.get_content())
        await self.session.message_extra.edit(content=msg_dump.attachments[0].url)

    def save_board_image(self):
        try:
            move = self.chessboard.peek()
            drawing = svg.board(self.chessboard, size=350, lastmove=move)
        except IndexError:
            drawing = svg.board(self.chessboard, size=350)
        f = open(f'{self.file}.svg', 'w')
        f.write(drawing)
        import os
        os.system(f'svgexport {self.file}.svg {self.file}.png 1.5x')

    def remove_files(self):
        import os
        os.remove(f"{self.file}.svg")
        os.remove(f"{self.file}.png")

    async def end_game(self):
        self.remove_files()
        await super().end_game()
