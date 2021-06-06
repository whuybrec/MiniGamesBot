import asyncio

from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.emojis import NUMBERS, STOP
from discordbot.utils.variables import TIMEOUT
from minigames.connect4 import Connect4


class Connect4Disc(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.connect4_game = Connect4()
        self.turn = self.connect4_game.turn

    async def start(self):
        await self.session.message.edit(content=self.get_content())

        for i in range(1, 8):
            await self.add_reaction(NUMBERS[i])
        await self.add_reaction(STOP)

        await self.wait_for_player(self.check)

    def check(self, r, u):
        return r.message.id == self.session.message.id \
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
        for n, e in NUMBERS.items():
            if e == reaction.emoji:
                self.connect4_game.move(n-1)

        await reaction.message.remove_reaction(reaction.emoji, user)
        self.turn = self.connect4_game.turn

        if self.connect4_game.has_player_won():
            self.winners.append(self.players[self.turn])
            self.losers.append(self.players[(self.turn + 1) % 2])
            self.playing = False

        if self.connect4_game.is_board_full():
            self.drawers.append(self.players[self.turn])
            self.drawers.append(self.players[(self.turn + 1) % 2])
            self.playing = False

        await self.session.message.edit(content=self.get_content())

    def get_content(self):
        board = self.connect4_game.get_board()
        content = "Board:\n"
        for i in range(1, 8):
            content += NUMBERS[i]

        content += "\n"
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    content += ":red_circle:"
                elif board[i][j] == 1:
                    content += ":yellow_circle:"
                else:
                    content += ":black_circle:"
            content += "\n"
        if not self.playing:
            if len(self.drawers) == 2:
                content += "\nGame ended in draw!"
            else:
                content += f"\n<@{str(self.winners[0].id)}> has won!"
        else:
            content += f"\nTurn: <@{str(self.players[self.turn].id)}>"
            if self.turn == 0:
                content += " :red_circle:"
            else:
                content += " :yellow_circle:"
        return content
