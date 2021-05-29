import asyncio

from Database.intent_daily_stats import Intent_daily_stats
from Database.intent_master import Intent_master
from discordbot.variables import Variables

class MiniGame:
    def __init__(self, bot, game_name, msg, player_id):
        self.bot = bot
        self.game_name = game_name
        self.msg = msg
        self.msg2 = msg
        self.player_id = player_id
        self.terminated = False
        self.wins = 0
        self.losses = 0
        self.draws = 0

        self.intent_master = Intent_master(self.msg.guild.id, self.player_id, game_name)
        self.intent_daily_stats = Intent_daily_stats(self.msg.guild.id, game_name)

    async def start_game(self):
        pass

    async def end_game(self):
        self.intent_master.add_scores(self.wins, self.losses, self.draws)
        self.intent_daily_stats.add_scores(self.wins, self.losses, self.draws)
        self.intent_master.commit()
        self.intent_daily_stats.commit()

    async def update_game(self, reaction, user):
        pass

    async def get_board(self):
        pass

    async def restart(self):
        try:
            await self.msg.clear_reactions()
        except Exception as e:
            await self.raise_exception(e)
        await self.msg2.clear_reactions()
        self.terminated = True
        await self.msg.add_reaction(Variables.REPEAT_EMOJI)
        try:
            r, u = await self.bot.wait_for('reaction_add',
                                                        check=lambda reaction, user:
                                                        reaction.emoji == Variables.REPEAT_EMOJI
                                                        and user.id == self.player_id and
                                                        reaction.message.id == self.msg.id,
                                                        timeout=Variables.TIMEOUT)
            await r.clear()
            self.terminated = False
            await self.start_game()
        except asyncio.TimeoutError:
            await self.msg.clear_reactions()
            await self.end_game()

    async def raise_exception(self, e):
        ctx = await self.bot.get_context(self.msg)
        await self.bot.on_command_error(ctx, e)

    def init_var(self):
        pass

    async def wait_for_player(self):
        try:
            reaction, user = await self.bot.wait_for("reaction_add",
                                                      check=lambda r, u: u.id == self.player_id and
                                                                         (r.message.id == self.msg.id or
                                                                          r.message.id == self.msg2.id),
                                                      timeout=Variables.TIMEOUT)
            await self.update_game(reaction, user)
        except asyncio.TimeoutError:
            try:
                await self.msg.clear_reactions()
            except Exception as e:
                await self.raise_exception(e)
            await self.msg2.clear_reactions()
            if not self.terminated:
                await self.end_game()

