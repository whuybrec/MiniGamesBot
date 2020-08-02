import discord
from Commands.minigame import MiniGame
from Minigames.chess.image_render import render
from string import ascii_lowercase
import random
import chess
import chess.svg


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

    def get_board(self):
        return render(self.board)

    async def update_game(self, content, author):
        if author.id not in self.players:
            return
        if self.players.index(author.id) != self.colors.index(self.turn):
            return

        point_a = content[:2]
        point_b = content[6:]
        s = point_a[0] + str(9 - int(point_a[1])) + point_b[0] + str(9 - int(point_b[1]))
        move = chess.Move.from_uci(s)
        if move in self.board.legal_moves:
            self.board.push(move)
        else:
            await self.msg.channel.send("Invalid move.")
            return  # your move fucked up, invalid move

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
            return  # check
        self.board_msg = await self.msg.channel.send("turn: <@" + str(self._players[self.turn]) + "> ("+self.turn+")",
                                                     file=discord.File(self.get_board(), filename="board.png"))

    def toggle_turn(self):
        if self.turn == "light":
            self.turn = "dark"
        else:
            self.turn = "light"
