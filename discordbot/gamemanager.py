import asyncio

import discord.errors

from discordbot.utils.emojis import *


class GameManager:
    bot = None

    open_sessions = list()
    paused_sessions = list()

    @classmethod
    def on_startup(cls, bot):
        cls.bot = bot

    @classmethod
    async def on_restart(cls):
        for session in cls.open_sessions:
            try:
                await session.message.edit(content=session.message.content+"\n\nSorry! I received an update and have to restart.")
                await session.message.clear_reactions()
                if session.message_extra is not None:
                    await session.message_extra.clear_reactions()
            except discord.errors.NotFound:
                await cls.bot.log_not_found(session)

        for session in cls.paused_sessions:
            try:
                await session.message.clear_reactions()
            except discord.errors.NotFound:
                await cls.bot.log_not_found(session)

    @classmethod
    def has_open_sessions(cls):
        return len(cls.open_sessions) > 0

    @classmethod
    def has_paused_sessions(cls):
        return len(cls.paused_sessions) > 0

    @classmethod
    async def start_session(cls, session):
        if cls.bot.has_update:
            try:
                await session.message.edit(content="Sorry! I can't start any new games right now. Boss says I have to restart soon:tm:. Try again later!")
            except discord.errors.NotFound:
                await cls.bot.log_not_found(session)
            return

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

        try:
            await session.message.edit(content=session.message.content + f"\n{session.get_summary()}")
            await session.message.add_reaction(STOP)
            await session.message.add_reaction(REPEAT)
        except discord.errors.NotFound:
            await cls.bot.log_not_found(session)
            await cls.end_session(session)
            return

        def check(r, u):
            return u.id in session.stats_players.keys() \
                   and (r.emoji == STOP or r.emoji == REPEAT) \
                   and r.message.id == session.message.id

        try:
            reaction, user = await cls.bot.wait_for('reaction_add', timeout=60.0, check=check)
            if reaction.emoji == STOP:
                await cls.end_session(session)
            elif reaction.emoji == REPEAT:
                await cls.start_session(session)
        except asyncio.TimeoutError:
            await cls.end_session(session)

