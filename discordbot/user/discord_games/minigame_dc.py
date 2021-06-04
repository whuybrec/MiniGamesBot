from discordbot.utils.variables import WIN, LOSE, DRAW


class MinigameDisc:
    def __init__(self, session):
        self.session = session
        self.status = -1
        self.emojis = set()

    async def end_game(self):
        await self.session.message.edit(content=self.get_content())
        await self.session.message.clear_reactions()
        self.emojis = set()
        if self.status == WIN:
            for v in self.session.stats_players.values():
                v["wins"] += 1
        elif self.status == LOSE:
            for v in self.session.stats_players.values():
                v["losses"] += 1
        elif self.status == DRAW:
            for v in self.session.stats_players.values():
                v["draws"] += 1
        await self.session.pause()

    async def add_reaction(self, emoji, extra=False):
        if not extra:
            await self.session.message.add_reaction(emoji)
        else:
            await self.session.message_extra.add_reaction(emoji)
        self.emojis.add(emoji)

    async def remove_reaction(self, emoji, user, extra=False):
        if not extra:
            await self.session.message.remove_reaction(emoji, user)
        else:
            await self.session.message_extra.remove_reaction(emoji, user)
        self.emojis.remove(emoji)

    async def clear_reaction(self, emoji, extra=False):
        if not extra:
            await self.session.message.clear_reaction(emoji)
        else:
            await self.session.message_extra.clear_reaction(emoji)
        self.emojis.remove(emoji)

    async def clear_reactions(self, extra=False):
        if not extra:
            await self.session.message.clear_reactions()
        else:
            await self.session.message_extra.clear_reactions()
        self.emojis = set()

    def get_content(self):
        pass
