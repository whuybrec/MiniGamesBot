import asyncio
import discord
from Minigames.minigame import MiniGame
from Minigames.chess.image_render import render
import random
import chess
import chess.svg
import re
from Other.variables import Variables


class Chess(MiniGame):
    def __init__(self, game_manager, msg, p1id, p2id):
        super().__init__(game_manager, msg)
        self.p1id = p1id
        self.p2id = p2id

        self.board = chess.Board()
        n = random.randint(1, 2)
        if n == 1:
            self.players = [self.p1id, self.p2id]
        else:
            self.players = [self.p2id, self.p1id]
        self.board_msg = None

        self.colors = ["light", "dark"]
        self._players = {"light": self.players[0], "dark": self.players[1]}
        self.turn = self.colors[0]

    async def start_game(self):
        self.board_msg = await self.msg.channel.send("<@" + str(self.players[0]) + "> is Light and can start, <@" +
                                                     str(self.players[1]) + "> is Dark",
                                                     file=discord.File(self.get_board(), filename="board.png"))
        await self.board_msg.add_reaction(Variables.STOP_EMOJI)
        await self.wait_for_player()

    def get_board(self):
        return render(self.board)

    async def update_game(self, message, author):
        if isinstance(message, discord.Reaction):
            if message.count != 2:
                return
            if message.message.id != self.board_msg.id:
                return
            if not author.id in self.players:
                return
            if message.emoji == Variables.STOP_EMOJI:
                await self.board_msg.edit(content="Game closed.")
                await self.end_game("chess")
                return
        if self.terminated:
            return
        if message.channel.id != self.msg.channel.id:
            await self.wait_for_player()
            return
        content = message.content
        if author.id not in self.players:
            await self.wait_for_player()
            return
        if self.players.index(author.id) != self.colors.index(self.turn):
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
            winner = self.players[self.colors.index(self.turn)]
            await self.msg.channel.send("Congratulations: <@" + str(winner) + "> won the game!",
                                        file=discord.File(self.get_board(), filename="board.png"))
            await self.end_game("chess")
            return  # player on turn won

        if self.board.is_stalemate():
            await self.msg.channel.send("It's a draw!",
                                        file=discord.File(self.get_board(), filename="board.png"))
            await self.end_game("chess")
            return  # draw

        self.toggle_turn()

        if self.board.is_check():
            player = self.players[self.colors.index(self.turn)]
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
        self.reschedule()
        try:
            msg = await self.game_manager.bot.wait_for("message",
                                                       check=lambda m: re.match(r"^[A-Ha-h][1-8] to [A-Ha-h][1-8]$",
                                                                                m.content.lower()) is not None,
                                                       timeout=Variables.TIMEOUT)
        except asyncio.TimeoutError:
            await self.end_game("chess")
            return
        await self.update_game(msg, msg.author)
