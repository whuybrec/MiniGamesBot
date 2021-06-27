from time import time

from discordbot.managers.messagemanager import MessageManager
from generic.stopwatch import Stopwatch

UPDATE_PENDING_CONTENT = "Sorry! I can't start any new games right now. Boss says I have to restart soon:tm:. Try again later!"


class Session:
    def __init__(self, message, game_name, handler):
        self.message = message
        self.game_name = game_name
        self.game_handler = handler

        self.stopwatch = Stopwatch()

        self.closed = False
        self.game = None
        self.extra_message = None
        self.update_pending = False
        self.last_seen = time()

    async def start_game(self):
        if self.update_pending:  # do not start game, bot update is pending
            await MessageManager.edit_message(self.message, UPDATE_PENDING_CONTENT)
            await self.close()
            return

        self.game = self.game_handler(self)
        self.stopwatch.start()

        await MessageManager.clear_reactions(self.message)
        try:
            await self.game.start_game()
        except Exception as e:
            await self.close()
            raise Exception(e)

    async def pause(self): pass

    async def close(self): pass

    async def is_inactive(self):
        if time() - self.last_seen > 60*5:
            await self.game.on_player_timed_out()
            return True

        return self.closed

    def update_last_seen(self):
        self.last_seen = time()

    async def on_restart(self):
        await MessageManager.edit_message(self.message, self.game.get_content() + "\n" + UPDATE_PENDING_CONTENT)
        await self.close()

    async def send_extra_message(self):
        if self.extra_message is None:
            self.extra_message = await self.message.channel.send("** **")
            self.game.extra_message = self.extra_message

    def get_summary(self): pass
