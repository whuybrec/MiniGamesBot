import asyncio
from Other.variables import Variables

class MiniGame:
    def __init__(self, game_manager, msg):
        self.game_manager = game_manager
        self.msg = msg
        self.msg2 = None
        self.board_msg = None
        self.receipt = Variables.scheduler.add(Variables.DEADLINE, self.deadline_reached)
        self.terminated = False

    async def start_game(self):
        pass

    async def end_game(self, game=None):
        try:
            self.terminated = True
            await self.msg.clear_reactions()
        except Exception as e:
            await self.raise_exception(e)
        await self.game_manager.close_game(self.msg, game)

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
        if self.terminated:
            return
        if self.msg.id in self.game_manager.open_games.keys():
            await self.msg.edit(content="Game closed, deadline reached.")
            if self.msg2 is not None:
                await self.msg2.delete()
            await self.end_game()
        elif self.msg.channel.id in self.game_manager.open_chess_games.keys():
            try:
                await self.board_msg.edit(content="Game closed, deadline reached.")
            except:
                await self.msg.edit(content="Game closed, deadline reached.")
            await self.end_game("chess")

    def reschedule(self):
        Variables.scheduler.cancel(self.receipt)
        self.receipt = Variables.scheduler.add(Variables.DEADLINE, self.deadline_reached)

    async def restart(self, game=None):
        self.terminated = True
        try:
            await self.msg.clear_reactions()
        except Exception as e:
            await self.raise_exception(e)
            return
        await self.msg.add_reaction(Variables.REPEAT_EMOJI)
        try:
            await self.game_manager.bot.wait_for('reaction_add',
                                                 check=lambda reaction, user: reaction.emoji == Variables.REPEAT_EMOJI
                                                 and user.id == self.player_id,
                                                 timeout=Variables.TIMEOUT)
            await self.msg.clear_reactions()
            await self.start_game()
        except asyncio.TimeoutError:
            await self.msg.clear_reactions()
            await self.end_game(game)

    async def raise_exception(self, e):
        ctx = await self.game_manager.bot.get_context(self.msg)
        await self.game_manager.bot.on_command_error(ctx, e)
