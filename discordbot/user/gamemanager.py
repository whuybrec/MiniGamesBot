import asyncio

from discordbot.utils.emojis import *


class GameManager:
    bot = None

    open_sessions = list()
    paused_sessions = list()

    @classmethod
    def on_startup(cls, bot):
        cls.bot = bot

    @classmethod
    async def start_session(cls, session):
        cls.open_sessions.append(session)
        if session in cls.paused_sessions:
            cls.paused_sessions.remove(session)
        await session.start()

    @classmethod
    async def end_session(cls, session):
        cls.paused_sessions.remove(session)
        await session.close()

    @classmethod
    async def pause_session(cls, session):
        cls.paused_sessions.append(session)
        cls.open_sessions.remove(session)

        await session.message.edit(content=session.message.content+f"{session.get_summary()}")
        await session.message.add_reaction(STOP)
        await session.message.add_reaction(REPEAT)

        def check(r, u):
            return u.id in session.stats_players.keys() and (r.emoji == STOP or r.emoji == REPEAT)

        try:
            reaction, user = await cls.bot.wait_for('reaction_add', timeout=60.0 * 5, check=check)

            if reaction.emoji == STOP:
                await cls.end_session(session)
            elif reaction.emoji == REPEAT:
                await cls.start_session(session)
        except asyncio.TimeoutError:
            await cls.end_session(session)

