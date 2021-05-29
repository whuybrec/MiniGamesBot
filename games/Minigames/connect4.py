#   [[0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0]]
#     0  1  2  3  4  5  6

import random
import copy
import numpy
from discordbot.variables import Variables
from games.Minigames.multiplayer_minigame import MultiMiniGame
import asyncio

coin = [1, 2]

class Connect4(MultiMiniGame):
    def __init__(self, bot, game_name, msg, players):
        super().__init__(bot, game_name, msg, players)
        self.terminated = False
        n = random.randint(0, 1)
        self.turn = n
        self.board = [[0 for x in range(7)] for y in range(6)]

    def get_board(self):
        return copy.deepcopy(self.board)

    def is_legal_move(self, c):
        if self.terminated:
            return False
        if c < 0 or c > 6:
            return False
        if self.board[0][c] != 0:
            return False
        return True

    def move(self, c, player_id):
        if self.is_legal_move(c):
            if self.board[5][c] == 0:
                self.board[5][c] = player_id
            else:
                for i in range(len(self.board)):
                    if self.board[i][c] != 0:
                        self.board[i - 1][c] = player_id
                        break
            if self.hasWon(player_id):
                self.terminated = True
                return 1
            self.toggle()
        if self.isFull():
            self.terminated = True
            return 2
        return 0

    def hasWon(self, player):
        checks = [self.checkH(player), self.checkV(player), self.checkD(player)]
        return sum(checks) > 0

    def checkH(self, player):
        for r in range(len(self.board)):
            for n in range(4):
                counter = 0
                for i in range(4):
                    if self.board[r][n + i] == player:
                        counter += 1
                if counter == 4:
                    return 1
        return 0

    def checkV(self, player):
        copyboard = copy.deepcopy(self.board)
        flipBoard = numpy.array(copyboard).transpose()
        for r in range(len(flipBoard)):
            for n in range(3):
                counter = 0
                for i in range(4):
                    if flipBoard[r][n + i] == player:
                        counter += 1
                if counter == 4:
                    return 1
        return 0

    def checkD(self, player):
        n = player
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                try:
                    if self.board[r][c] == n:
                        if self.board[r + 1][c + 1] == n:
                            if self.board[r + 2][c + 2] == n:
                                if self.board[r + 3][c + 3] == n:
                                    return 1
                except IndexError:
                    pass
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                try:
                    if not (c - 3) < 0 and self.board[r][c] == n:
                        if self.board[r + 1][c - 1] == n:
                            if self.board[r + 2][c - 2] == n:
                                if self.board[r + 3][c - 3] == n:
                                    return 1
                except IndexError:
                    pass
        return 0

    def isFull(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return False
        return True

    def updateBoard(self):
        text = "Board: \n"
        board = self.get_board()
        text += "1⃣" + "2⃣" + "3⃣" + "4⃣" + "5⃣" + "6⃣" + "7⃣" + "\n"
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == self.players[0].id:
                    text += ":red_circle:"
                elif board[i][j] == self.players[1].id:
                    text += ":yellow_circle:"
                else:
                    text += ":black_circle:"
            text += "\n"
        text += "\nTurn: <@" + str(self.players[self.turn].id) + ">"
        return text

    def toggle(self):
        self.turn = (self.turn + 1) % 2

    async def start_game(self):
        await self.msg.edit(content=self.updateBoard())
        for emo in Variables.REACTIONS_CONNECT4:
            await self.msg.add_reaction(emo)

        await self.wait_for_player()

    async def update_game(self, reaction, user):
        if self.terminated:
            return

        if reaction.emoji in Variables.REACTIONS_CONNECT4:
            res = self.move(Variables.REACTIONS_CONNECT4.index(reaction.emoji), user.id)
            text = self.updateBoard()
            await reaction.message.edit(content=text)

            if res == 1:  # A player has won
                await reaction.message.channel.send("<@" + str(user.id) + "> has won!")
                self.index_winner = self.turn
                await self.end_game()
                return

            if res == 2:  # There is no winner, board is full
                self.index_winner = -1
                await reaction.message.channel.send("<@" + str(self.players[0].id) + "> and <@" + str(
                    self.players[1].id) + "> drawed because the board is full.")
                await self.end_game()
                return

        await reaction.message.remove_reaction(reaction.emoji, user)
        await self.wait_for_player()

    async def wait_for_player(self):
        try:
            reaction, user = await self.bot.wait_for("reaction_add",
                                                                  check=lambda r, u: u.id == self.players[self.turn].id
                                                                                     and r.message.id == self.msg.id,
                                                                  timeout=Variables.TIMEOUT)
            await self.update_game(reaction, user)
        except asyncio.TimeoutError:
            await self.end_game(True)
