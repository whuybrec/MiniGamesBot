import asyncio
import random
import re

import chess.svg
import discord

import chess
from discordbot.user.variables import Variables
from minigames.Minigames.chess.image_render import render
from minigames.Minigames.multiplayer_minigame import MultiMiniGame


class Chess(MultiMiniGame):
    def __init__(self, bot, game_name, msg, players):
        super().__init__(bot, game_name, msg, players)
        self.p1id = players[0].id
        self.p2id = players[1].id
        self.board = chess.Board()
        self.board_msg = None

        self.colors = ["light", "dark"]
        n = random.randint(0, 1)
        self._players = {"light": self.players[n].id, "dark": self.players[(n+1)%2].id}
        self.turn = "light"

    async def start_game(self):
        self.board_msg = await self.msg.channel.send("<@" + str(self._players[self.turn]) + "> is Light and can start",
                                                     file=discord.File(self.get_board(), filename="board.png"))
        await self.board_msg.add_reaction(Variables.STOP_EMOJI)
        await self.wait_for_player()

    def get_board(self):
        return render(self.board)

    async def update_game(self, message, author):
        if self.terminated:
            return
        if message.channel.id != self.msg.channel.id:
            await self.wait_for_player()
            return

        content = message.content.lower()
        if author.id != self.p1id and author.id != self.p2id:
            await self.wait_for_player()
            return
        if author.id != self._players[self.turn]:
            await self.wait_for_player()
            return

        point_a = content[:2]
        point_b = content[6:]
        s = point_a[0] + str(9 - int(point_a[1])) + point_b[0] + str(9 - int(point_b[1]))
        move = chess.Move.from_uci(s)
        if move in self.board.legal_moves:
            self.board.push(move)
        else:
            await self.msg.channel.send("Invalid move.")
            await self.wait_for_player()
            return

        if self.board.is_checkmate():
            winner = self._players[self.turn]
            if self.p1id == winner:
                self.index_winner = 0
            else:
                self.index_winner = 1
            await self.msg.channel.send("Congratulations: <@" + str(winner) + "> won the game!",
                                        file=discord.File(self.get_board(), filename="board.png"))
            await self.end_game()
            return  # player on turn won

        if self.board.is_stalemate():
            self.index_winner = -1
            await self.msg.channel.send("It's a draw!",
                                        file=discord.File(self.get_board(), filename="board.png"))
            await self.end_game()
            return

        self.toggle_turn()

        if self.board.is_check():
            player = self.players[self.colors.index(self.turn)].id
            self.board_msg = await self.msg.channel.send("CHECK on " + self.turn + " king!\n"
                                                                                   "turn: <@" + str(player) + ">",
                                                         file=discord.File(self.get_board(), filename="board.png"))
            await self.board_msg.add_reaction(Variables.STOP_EMOJI)
        else:
            self.board_msg = await self.msg.channel.send("turn: <@" + str(self._players[self.turn]) +
                                                         "> (" + self.turn + ")",
                                                         file=discord.File(self.get_board(), filename="board.png"))
            await self.board_msg.add_reaction(Variables.STOP_EMOJI)
        await self.wait_for_player()

    def toggle_turn(self):
        if self.turn == "light":
            self.turn = "dark"
        else:
            self.turn = "light"

    async def wait_for_player(self):
        do_a = asyncio.create_task(self.await_reaction())
        do_b = asyncio.create_task(self.await_message())

        done, pending = await asyncio.wait([do_a, do_b], return_when=asyncio.FIRST_COMPLETED)

        if do_b in done:
            msg = do_b.result()
            if msg is None: return
            await self.update_game(msg, msg.author)
        elif do_a in done:
            await self.board_msg.edit(content="Game closed.")
            await self.end_game(True)

    async def await_message(self):
        try:
            message = await self.bot.wait_for("message", check=lambda m: re.match(r"^[A-Ha-h][1-8] to [A-Ha-h][1-8]$",
                                                                                 m.content) is not None,
                                             timeout=Variables.TIMEOUT)
            return message
        except asyncio.TimeoutError:
            await self.end_game(True)
            return None

    async def await_reaction(self):
        reaction, user = await self.bot.wait_for("reaction_add", check=lambda r, u: u.id in self._players.values() and
                                                                              r.message.id == self.board_msg.id and
                                                              r.emoji == Variables.STOP_EMOJI)
        return reaction, user