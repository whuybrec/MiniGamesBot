from discordbot.discordminigames.discordminigame import DiscordMinigame
from discordbot.managers.messagemanager import MessageManager

PLAYING = 0     # player playing the game
WON = 1         # player has won the game
DRAW = 3        # player has drawn in the game
QUIT = 4        # player force quit the game or was idle for too long


class MultiPlayerGame(DiscordMinigame):
    def __init__(self, session):
        self.session = session
        self.message = self.session.message
        self.extra_message = self.session.extra_message
        self.players = self.session.players
        self.game_state = PLAYING
        self.turn = None

    async def start_game(self): pass

    async def end_game(self):
        self.players[0].played()
        self.players[1].played()

        if self.game_state == WON:
            self.players[self.turn].win()
            self.players[self.turn-1].lose()
        elif self.game_state == DRAW:
            self.players[self.turn].draw()
            self.players[self.turn - 1].draw()
        elif self.game_state == QUIT:
            self.players[0].did_not_finish()
            self.players[1].did_not_finish()
            self.players[self.turn].lose()
            self.players[self.turn - 1].win()

        await self.clear_reactions()
        await self.session.pause()

    async def on_player_timed_out(self):
        self.game_state = QUIT
        await self.end_game()

    async def on_quit_game(self, player):
        self.turn = self.players.index(player)
        self.game_state = QUIT
        await self.end_game()

    def on_end_move(self): pass

    def on_start_move(self):
        self.update_last_seen()

    def get_board(self): pass

    def update_last_seen(self):
        self.session.update_last_seen()

    async def clear_reactions(self):
        await MessageManager.clear_reactions(self.message)
        if self.extra_message is not None:
            await MessageManager.clear_reactions(self.extra_message)

    async def game_won(self):
        self.game_state = WON
        await self.end_game()

    async def game_draw(self):
        self.game_state = DRAW
        await self.end_game()
