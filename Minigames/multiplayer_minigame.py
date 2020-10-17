from Database.intent_daily_stats import Intent_daily_stats
from Database.intent_master import Intent_master


class MultiMiniGame:
    def __init__(self, bot, game_name, msg, players):
        self.bot = bot
        self.game_name = game_name
        self.msg = msg
        self.players = players
        self.index_winner = -2
        self.terminated = False

        self.intents_master = []
        self.intent_d = Intent_daily_stats(self.msg.guild.id, game_name)

        for player in players:
            intent_m = Intent_master(self.msg.guild.id, player.id, game_name)
            self.intents_master.append(intent_m)

    async def start_game(self):
        pass

    async def end_game(self, timeout=False):
        self.terminated = True
        self.save_intents(timeout)
        try:
            await self.msg.clear_reactions()
        except Exception as e:
            await self.raise_exception(e)

    async def update_game(self, reaction, user):
        pass

    async def raise_exception(self, e):
        ctx = await self.bot.get_context(self.msg)
        await self.bot.on_command_error(ctx, e)

    def save_intents(self, timeout):
        if self.index_winner == -1: # game is a draw
            for i in range(len(self.players)):
                self.intents_master[i].add_scores(0, 0, 1)
            self.intent_d.add_scores(0, 0, len(self.players))
        elif 0 <= self.index_winner: # game has a winner and losers
            self.intent_d.add_scores(1, len(self.players)-1, 0)
            for i in range(len(self.players)):
                if i == self.index_winner:
                    self.intents_master[i].add_scores(1, 0, 0)
                else:
                    self.intents_master[i].add_scores(0, 1, 0)

        for i in range(len(self.players)):
            self.intents_master[i].commit(timeout)
        self.intent_d.commit(timeout)