from discordbot.user.variables import WIN, LOSE
from discordbot.utils.emojis import STOP


class MinigameDisc:
    def __init__(self, session):
        self.session = session
        self.status = -1
        self.emojis = set()

    @staticmethod
    def has_pressed_stop(reaction):
        if reaction.emoji == STOP:
            return True
        return False

    async def validate(self, reaction, user):
        if reaction.emoji not in self.emojis:
            await self.session.message.clear_reaction(reaction.emoji)
            return False

        if user.id != self.session.context.author.id and user.id != self.session.message.author.id:
            await self.session.message.remove_reaction(reaction.emoji, user)
            return False
        return True

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
        await self.session.pause()

    def get_content(self):
        pass
