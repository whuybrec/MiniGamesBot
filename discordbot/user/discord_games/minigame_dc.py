from discordbot.messagemanager import MessageManager

TIMEOUT = 60*5


class MinigameDisc:
    def __init__(self, session):
        self.session = session
        self.scheduler = self.session.scheduler
        self.message = self.session.message
        self.extra_message = self.session.extra_message
        self.players = self.session.players

        self.turn = 0
        self.ticket = None
        self.finished = False

    async def start_game(self):
        raise NotImplementedError

    async def end_game(self):
        self.finished = True
        await MessageManager.edit_message(self.message, self.get_content() + "\n" + self.session.get_summary())
        await self.clear_reactions()
        await self.session.pause()

    def get_content(self):
        raise NotImplementedError

    async def on_stop_reaction(self):
        self.cancel_timer()
        self.players[self.turn].losses += 1
        await self.end_game()

    async def on_bot_restart(self):
        await self.clear_reactions()
        await MessageManager.edit_message(self.message,
                                          self.get_content() + "\n\nSorry! I received an update and have to restart.")

    async def clear_reactions(self):
        await MessageManager.clear_reactions(self.message)
        if self.extra_message is not None:
            await MessageManager.clear_reactions(self.extra_message)

    async def on_player_timed_out(self):
        self.players[self.turn].unfinished += 1
        self.players[self.turn].losses += 1
        await self.end_game()

    def start_timer(self):
        self.ticket = self.scheduler.add(TIMEOUT, self.on_player_timed_out)

    def cancel_timer(self):
        self.session.scheduler.cancel(self.ticket)
