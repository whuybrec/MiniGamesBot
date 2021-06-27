from discordbot.discordminigames.multiplayergames.multiplayergame import MultiPlayerGame, WON, DRAW
from discordbot.managers.messagemanager import MessageManager
from discordbot.utils.emojis import NUMBERS, STOP
from minigames.connect4 import Connect4


class Connect4Discord(MultiPlayerGame):
    def __init__(self, session):
        super().__init__(session)
        self.connect4_game = Connect4()
        self.turn = self.connect4_game.turn

    async def start_game(self):
        await MessageManager.edit_message(self.message, self.get_board())

        for i in range(1, 8):
            await MessageManager.add_reaction_and_event(self.message, NUMBERS[i], self.players[self.turn].id,
                                                        self.on_number_reaction,
                                                        NUMBERS[i], self.players[self.turn].id)

        await MessageManager.add_reaction_and_event(self.message, STOP, self.players[0].id, self.on_quit_game, self.players[0])
        await MessageManager.add_reaction_event(self.message, STOP, self.players[1].id, self.on_quit_game, self.players[1])

    async def on_number_reaction(self, number_emoji, user_id):
        if user_id != self.players[self.turn].id:
            return

        self.on_start_move()

        for number, emoji in NUMBERS.items():
            if emoji == number_emoji:
                self.connect4_game.move(number - 1)
                break

        self.turn = self.connect4_game.turn
        await MessageManager.remove_reaction(self.message, number_emoji, self.players[self.turn].member)

        if self.connect4_game.has_player_won():
            await self.game_won()
            return

        if self.connect4_game.is_board_full():
            await self.game_draw()
            return

        await MessageManager.edit_message(self.message, self.get_board())

        for i in range(1, 8):
            await MessageManager.remove_reaction_event(self.message, NUMBERS[i], self.players[self.turn-1].id)
            await MessageManager.add_reaction_event(self.message, NUMBERS[i], self.players[self.turn].id,
                                                    self.on_number_reaction,
                                                    NUMBERS[i], self.players[self.turn].id)

    def get_board(self):
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

        if self.game_state == WON:
            content += f"\n<@{str(self.players[self.turn].id)}> has won!"
        elif self.game_state == DRAW:
            content += "\nGame ended in draw!"
        else:
            content += f"\nTurn: <@{str(self.players[self.turn].id)}>"
            if self.turn == 0:
                content += " :red_circle:"
            else:
                content += " :yellow_circle:"
        return content
