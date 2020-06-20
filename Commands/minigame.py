from Other.variables import scheduler, Variables

class MiniGame:
    def __init__(self, game_manager, msg):
        self.game_manager = game_manager
        self.msg = msg
        self.msg2 = None
        Variables.scheduler.add(Variables.DEADLINE, self.deadline_reached)

    async def start_game(self):
        pass

    async def end_game(self):
        await self.msg.clear_reactions()
        await self.game_manager.close_game(self.msg.id)

    async def update_game(self, reaction, user):
        pass

    async def get_board(self):
        pass

    async def force_quit(self):
        await self.msg.edit(content="Game closed because the dev is restarting the bot.")
        await self.msg.clear_reactions()
        if self.msg2 is not None:
            await self.msg2.delete()

    async def deadline_reached(self):
        await self.msg.edit(content="Game closed, deadline reached.")
        if self.msg2 is not None:
            await self.msg2.delete()
        await self.end_game()