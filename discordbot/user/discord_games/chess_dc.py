import asyncio
import random
from string import ascii_lowercase

import chess
import discord
from discordbot.utils.private import DISCORD
from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.user.variables import TIMEOUT, WIN, LOSE, DRAW
from discordbot.utils.emojis import ALPHABET, STOP, NUMBERS, ARROW_LEFT_2
from chess import Board, svg

# TURN: 0 WHITE
# TURN: 1 BLACK


class ChessDisc(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.chessboard = Board()
        self.player_ids = [p.id for p in self.session.players]
        self.turn = 0
        self.move = ""
        self.choosing_letter = True
        self.choosing_number = False
        self.id = random.getrandbits(64)
        self.file = f'bin/{self.id}'
        random.shuffle(self.player_ids)

    async def start(self):
        await self.update_messages()

        for i in range(8):
            await self.add_reaction(ALPHABET[ascii_lowercase[i]])
        for i in range(1, 9):
            await self.add_reaction(NUMBERS[i], True)

        await self.add_reaction(ARROW_LEFT_2, True)
        await self.add_reaction(STOP, True)

        await self.wait_for_player()

    async def wait_for_player(self):
        def check(r, u):
            return r.message.id in [self.session.message.id, self.session.message_extra.id] \
                   and r.emoji in self.emojis \
                   and u.id == self.player_ids[self.turn]

        try:
            while True:
                reaction, user = await self.session.bot.wait_for("reaction_add", check=check, timeout=TIMEOUT)

                if reaction.emoji == STOP:
                    self.status = LOSE
                    break

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
                        self.next_turn()
                        self.move = ""
                        await self.update_messages()
                    else:
                        self.move = ""
                        await self.session.message.edit(content=self.get_content()+"\nIncorrect move, try again!")

                if self.chessboard.is_checkmate():
                    self.status = LOSE
                    break

                elif self.chessboard.is_stalemate() or self.chessboard.is_insufficient_material():
                    self.status = DRAW
                    break

        except asyncio.TimeoutError:
            self.status = LOSE

        await self.end_game()

    def get_content(self):
        if self.status != -1:
            if self.status == LOSE:
                content = f"<@{str(self.player_ids[(self.turn+1)%2])}> won the game!"
            else:
                content = f"Game ended in draw!"
        else:
            if self.turn == 0:
                color = "White"
            else:
                color = "Black"
            content = f"{color}'s turn: <@{str(self.player_ids[self.turn])}>\n"
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

    def next_turn(self):
        self.turn = (self.turn+1) % 2

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
        await self.update_messages()
        await self.session.message.clear_reactions()
        await self.session.message_extra.clear_reactions()
        self.remove_files()

        self.emojis = set()
        if self.status == LOSE:  # player with turn lost
            for p_id in self.session.stats_players.keys():
                if p_id == self.player_ids[self.turn]:
                    self.session.stats_players[p_id]["losses"] += 1
                else:
                    self.session.stats_players[p_id]["wins"] += 1
        elif self.status == DRAW:  # players draw
            for p_id in self.session.stats_players.keys():
                self.session.stats_players[p_id]["draws"] += 1
        await self.session.pause()
