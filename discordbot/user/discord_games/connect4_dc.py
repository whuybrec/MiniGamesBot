from discordbot.messagemanager import MessageManager
from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.emojis import NUMBERS, STOP
from minigames.connect4 import Connect4


class Connect4Discord(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.connect4_game = Connect4()
        self.turn = self.connect4_game.turn

    async def start_game(self):
        await MessageManager.edit_message(self.message, self.get_content())

        for i in range(1, 8):
            await MessageManager.add_reaction_event(self.message, NUMBERS[i], self.players[self.turn].id,
                                                    self.on_number_reaction, NUMBERS[i])

        await MessageManager.add_reaction_event(self.message, STOP, self.players[0].id, self.on_stop_reaction)
        await MessageManager.add_reaction_event(self.message, STOP, self.players[1].id, self.on_stop_reaction)

        self.start_timer()

    async def on_number_reaction(self, number_emoji):
        self.cancel_timer()

        for number, emoji in NUMBERS.items():
            if emoji == number_emoji:
                self.connect4_game.move(number - 1)
                break

        old_turn = self.turn
        self.turn = self.connect4_game.turn
        await MessageManager.remove_reaction(self.message, number_emoji, self.players[old_turn].member)

        if self.connect4_game.has_player_won():
            self.players[self.turn].wins += 1
            self.players[(self.turn + 1) % 2].losses += 1
            await self.end_game()
            return

        if self.connect4_game.is_board_full():
            self.players[self.turn].draws += 1
            self.players[(self.turn + 1) % 2].draws += 1
            await self.end_game()
            return

        for i in range(1, 8):
            await MessageManager.add_reaction_event(self.message, NUMBERS[i], self.players[self.turn].id,
                                                    self.on_number_reaction, NUMBERS[i])
            await MessageManager.remove_reaction_event(self.message.id, NUMBERS[i], self.players[old_turn].id)

        await MessageManager.edit_message(self.message, self.get_content())

        self.start_timer()

    async def on_stop_reaction(self):
        self.cancel_timer()
        self.players[self.turn].losses += 1
        self.players[(self.turn + 1) % 2].wins += 1
        await self.end_game()

    async def on_player_timed_out(self):
        self.players[self.turn].unfinished += 1
        self.players[(self.turn + 1) % 2].unfinished += 1
        self.players[self.turn].losses += 1
        self.players[(self.turn + 1) % 2].wins += 1
        await self.end_game()

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
        if self.finished:
            if self.connect4_game.is_board_full():
                content += "\nGame ended in draw!"
            else:
                content += f"\n<@{str(self.players[self.turn].id)}> has won!"
        else:
            content += f"\nTurn: <@{str(self.players[self.turn].id)}>"
            if self.turn == 0:
                content += " :red_circle:"
            else:
                content += " :yellow_circle:"
        return content
