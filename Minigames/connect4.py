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
from Other.variables import Variables
from Other.private import Private
from Minigames.minigame import MiniGame

coin = [1, 2]
class Connect4(MiniGame):
    def __init__(self, game_manager, msg, p1, p2):
        super().__init__(game_manager, msg)
        self.p1start = False
        self.p2start = False
        self.finished = False
        n = random.randint(1,2)
        if n == 1:
            self.players = [p1, p2]
        else:
            self.players = [p2, p1]
        self.turn = self.players[0]
        self.board = [[0 for x in range(7)] for y in range(6)]

    def getTurn(self):
        return self.turn

    def getBoard(self):
        return copy.deepcopy(self.board)

    def getPlayers(self):
        return self.players

    def isLegalMove(self, c, player):
        if player not in self.players:
            raise Exception("Illegal player: " + str(player) + " is not part of the game")
        if self.finished:
            raise Exception("Illegal move: game is finished")
        if self.turn != player:
            raise Exception("Illegal move: not your turn to play "+ str(player))
        if c < 0 or c > 6:
            raise Exception("Illegal column: columns ∈ [0,6], your move was " + str(c))
        if self.board[0][c] != 0:
            raise Exception("Illegal row: row is full")
        return True

    def move(self, c, player):
        if self.isLegalMove(c, player):
            if self.board[5][c] == 0:
                self.board[5][c] = player
            else:
                for i in range(len(self.board)):
                    if self.board[i][c] != 0:
                        self.board[i-1][c] = player
                        break
            if self.hasWon(player):
                self.finished = True
                return 1
            self.turn = self.players[(self.players.index(player)+1)%2]
        if self.isFull():
            self.finished = True
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
                    if self.board[r][n+i] == player:
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
                        if self.board[r+1][c+1] == n:
                            if self.board[r+2][c+2] == n:
                                if self.board[r+3][c+3] == n:
                                    return 1
                except:
                    pass
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                try:
                    if self.board[r][c] == n:
                        if self.board[r + 1][c - 1] == n:
                            if self.board[r + 2][c - 2] == n:
                                if self.board[r + 3][c - 3] == n:
                                    return 1
                except:
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
        board = self.getBoard()
        players = self.getPlayers()
        text += "1⃣"+"2⃣"+"3⃣"+"4⃣"+"5⃣"+"6⃣"+"7⃣"+"\n"
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == players[0]:
                    text += ":red_circle:"
                elif board[i][j] == players[1]:
                    text += ":yellow_circle:"
                else:
                    text += ":black_circle:"
            text += "\n"
        text += "\nTurn: <@" + str(self.getTurn())+">"
        return text


    def toggle(self, uid):
        index = self.players.index(uid)
        if index == 0:
            self.p1start = True
        else:
            self.p2start = True

    async def start_game(self):
        await self.msg.edit(content=self.updateBoard())
        for emo in Variables.REACTIONS_CONNECT4:
            await self.msg.add_reaction(emo)

    async def update_game(self, reaction, user):
        if reaction.message.author.id not in Private.BOT_ID: return
        if user.id in Private.BOT_ID: return
        if not user.id in self.getPlayers():
            await reaction.message.remove_reaction(reaction.emoji, user)
            return
        try:
            if reaction.emoji in Variables.REACTIONS_CONNECT4:
                self.toggle(user.id)
                res = self.move(Variables.REACTIONS_CONNECT4.index(reaction.emoji), user.id)
                text = self.updateBoard()
                await reaction.message.edit(content=text)

                if res == 1: # A player has won
                    await reaction.message.channel.send("<@" + str(user.id) + "> has won!")
                    await self.end_game()
                    return

                if res == 2: # There is no winner, board is full
                    await reaction.message.channel.send("<@"+str(self.players[0])+"> and <@"+ str(self.players[1]) + "> drawed because the board is full.")
                    await self.end_game()
                    return
        except:
            pass
        await reaction.message.remove_reaction(reaction.emoji, user)
