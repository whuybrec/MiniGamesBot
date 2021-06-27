from discordbot.discordminigames.discordminigame import DiscordMinigame
from discordbot.managers.messagemanager import MessageManager

PLAYING = 0     # player playing the game
WON = 1         # player has won the game
LOST = 2        # player has lost the game
DRAW = 3        # player has drawn in the game
QUIT = 4        # player force quit the game or was idle for too long
UNFINISHED = 5


class SinglePlayerGame(DiscordMinigame):
    def __init__(self, session):
        self.session = session
        self.message = self.session.message
        self.extra_message = self.session.extra_message
        self.player = self.session.player
        self.game_state = PLAYING

    async def start_game(self): pass

    async def end_game(self):
        self.player.played()
        if self.game_state == WON:
            self.player.win()
        elif self.game_state == LOST:
            self.player.lose()
        elif self.game_state == DRAW:
            self.player.draw()
        elif self.game_state == QUIT:
            self.player.did_not_finish()
            self.player.lose()
        elif self.game_state == UNFINISHED:
            self.player.did_not_finish()

        await self.clear_reactions()
        await self.session.pause()

    async def on_player_timed_out(self):
        await self.on_quit_game()

    async def on_quit_game(self):
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

    async def game_lost(self):
        self.game_state = LOST
        await self.end_game()

    async def game_draw(self):
        self.game_state = DRAW
        await self.end_game()
