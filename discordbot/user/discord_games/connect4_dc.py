import asyncio
import random
from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.user.variables import LOSE, WIN, DRAW, TIMEOUT
from discordbot.utils.emojis import NUMBERS, STOP
from minigames.connect4 import Connect4


class Connect4Disc(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.connect4_game = Connect4()
        self.player_ids = [p.id for p in self.session.players]
        random.shuffle(self.player_ids)

    async def start(self):
        await self.session.message.edit(content=self.get_content())

        for i in range(1, 8):
            await self.add_reaction(NUMBERS[i])
        await self.add_reaction(STOP)

        await self.wait_for_player()

    async def wait_for_player(self):
        def check(r, u):
            return r.message.id == self.session.message.id \
                   and r.emoji in self.emojis \
                   and u.id == self.player_ids[self.connect4_game.turn]

        try:
            while True:
                reaction, user = await self.session.bot.wait_for("reaction_add", check=check, timeout=TIMEOUT)
                if reaction.emoji == STOP:
                    self.status = LOSE
                    break

                for n, e in NUMBERS.items():
                    if e == reaction.emoji:
                        self.connect4_game.move(n-1)

                await reaction.message.remove_reaction(reaction.emoji, user)

                if self.connect4_game.has_player_won():
                    self.status = WIN
                    break

                if self.connect4_game.is_board_full():
                    self.status = DRAW
                    break

                await self.session.message.edit(content=self.get_content())

        except asyncio.TimeoutError:
            self.status = LOSE

        await self.end_game()

    async def end_game(self):
        await self.session.message.edit(content=self.get_content())
        await self.session.message.clear_reactions()
        self.emojis = set()
        if self.status == WIN:  # player with turn won
            for p_id in self.session.stats_players.keys():
                if p_id == self.player_ids[self.connect4_game.turn]:
                    self.session.stats_players[p_id]["wins"] += 1
                else:
                    self.session.stats_players[p_id]["losses"] += 1
        elif self.status == LOSE:  # player with turn lost
            for p_id in self.session.stats_players.keys():
                if p_id == self.player_ids[self.connect4_game.turn]:
                    self.session.stats_players[p_id]["losses"] += 1
                else:
                    self.session.stats_players[p_id]["wins"] += 1
        elif self.status == DRAW:  # players draw
            for p_id in self.session.stats_players.keys():
                self.session.stats_players[p_id]["draws"] += 1
        await self.session.pause()

    async def validate(self, reaction, user):
        if reaction.emoji not in self.emojis:
            await self.session.message.clear_reaction(reaction.emoji)
            return False

        if user.id != self.player_ids[self.connect4_game.turn] and user.id != self.session.message.author.id:
            await self.session.message.remove_reaction(reaction.emoji, user)
            return False
        return True

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
        if self.status == WIN:
            content += f"\n<@{str(self.player_ids[self.connect4_game.turn])}> has won!"
        elif self.status == LOSE:
            content += f"\n<@{str(self.player_ids[self.connect4_game.turn])}> has lost!"
        elif self.status == DRAW:
            content += "\nGame ended in draw!"
        else:
            content += f"\nTurn: <@{str(self.player_ids[self.connect4_game.turn])}>"
            if self.connect4_game.turn == 0:
                content += " :red_circle:"
            else:
                content += " :yellow_circle:"
        return content
