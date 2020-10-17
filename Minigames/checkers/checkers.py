import asyncio
import discord
from Minigames.multiplayer_minigame import MultiMiniGame
from Minigames.checkers.image_render import render
import random
from checkers.game import Game
import re
from Other.variables import Variables
from string import ascii_lowercase

abs_rel_pos = {"01": 1, "03": 2, "05": 3, "07": 4, "10": 5, "12": 6, "14": 7, "16": 8, "21": 9, "23": 10, "25": 11,
               "27": 12, "30": 13, "32": 14, "34": 15, "36": 16, "41": 17, "43": 18, "45": 19, "47": 20, "50": 21,
               "52": 22, "54": 23, "56": 24, "61": 25, "63": 26, "65": 27, "67": 28, "70": 29, "72": 30, "74": 31, "76": 32, }



class Checkers(MultiMiniGame):
    def __init__(self, bot, game_name, msg, players):
        super().__init__(bot, game_name, msg, players)
        self.p1id = players[0].id
        self.p2id = players[1].id
        self.game = Game()
        self.last_turn = self.game.whose_turn()
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
        return render(self.game)

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
        n = ascii_lowercase.index(content[:2][0])
        x = str(8 - int(content[:2][1])) + str(n)
        n = ascii_lowercase.index(content[6:][0])
        y = str(8 - int(content[6:][1])) + str(n)

        try:
            move = [abs_rel_pos[x], abs_rel_pos[y]]
        except KeyError:
            await self.msg.channel.send("Invalid move.")
            await self.wait_for_player()
            return

        moves = self.game.get_possible_moves()
        if move in moves:
            self.game.move(move)
        else:
            await self.msg.channel.send("Invalid move.")
            await self.wait_for_player()
            return

        if self.game.is_over():
            winner = self._players[self.turn]
            if self.p1id == winner:
                self.index_winner = 0
            else:
                self.index_winner = 1
            await self.msg.channel.send("Congratulations: <@" + str(winner) + "> won the game!",
                                        file=discord.File(self.get_board(), filename="board.png"))
            await self.end_game()
            return  # player on turn won

        self.toggle_turn()

        self.board_msg = await self.msg.channel.send("turn: <@" + str(self._players[self.turn]) +
                                                     "> (" + self.turn + ")",
                                                     file=discord.File(self.get_board(), filename="board.png"))
        await self.board_msg.add_reaction(Variables.STOP_EMOJI)
        await self.wait_for_player()


    def toggle_turn(self):
        new_turn = self.game.whose_turn()
        if self.last_turn == new_turn:
            return
        else:
            self.last_turn = new_turn
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