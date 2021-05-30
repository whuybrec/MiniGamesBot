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
