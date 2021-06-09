import asyncio

import discord.errors

from discordbot.utils.emojis import STOP
from discordbot.utils.variables import TIMEOUT


class MinigameDisc:
    def __init__(self, session):
        self.session = session
        self.emojis = set()
        self.players = session.players
        self.winners = []
        self.losers = []
        self.drawers = []
        self.playing = True
        self.turn = 0

    async def add_reaction(self, emoji, extra=False):
        try:
            if not extra:
                await self.session.message.add_reaction(emoji)
            else:
                await self.session.message_extra.add_reaction(emoji)
        except Exception as e:
            await self.session.bot.on_command_error(self.session.context, e)
        self.emojis.add(emoji)

    async def remove_reaction(self, emoji, user, extra=False):
        try:
            if not extra:
                await self.session.message.remove_reaction(emoji, user)
            else:
                await self.session.message_extra.remove_reaction(emoji, user)
        except Exception as e:
            await self.session.bot.on_command_error(self.session.context, e)
        self.emojis.remove(emoji)

    async def clear_reaction(self, emoji, extra=False):
        try:
            if not extra:
                await self.session.message.clear_reaction(emoji)
            else:
                await self.session.message_extra.clear_reaction(emoji)
        except Exception as e:
            await self.session.bot.on_command_error(self.session.context, e)
        self.emojis.remove(emoji)

    async def clear_reactions(self, extra=False):
        try:
            if not extra:
                await self.session.message.clear_reactions()
            else:
                await self.session.message_extra.clear_reactions()
        except Exception as e:
            await self.session.bot.on_command_error(self.session.context, e)
        self.emojis = set()

    def get_content(self):
        pass

    async def wait_for_player(self, check_=None):
        def check(r, u):
            return r.message.id == self.session.message.id \
                   and r.emoji in self.emojis \
                   and u.id == self.players[self.turn].id

        while self.playing:
            try:
                if check_ is None:
                    reaction, user = await self.session.bot.wait_for("reaction_add", check=check, timeout=TIMEOUT)
                else:
                    reaction, user = await self.session.bot.wait_for("reaction_add", check=check_, timeout=TIMEOUT)
                if reaction.emoji == STOP:
                    self.losers.append(self.players[0])
                    self.session.player_timed_out = self.players[self.turn].id
                    self.playing = False

                await self.on_reaction(reaction, user)

            except asyncio.TimeoutError:
                self.losers.append(self.players[0])
                self.session.player_timed_out = self.players[self.turn].id
                self.playing = False
        try:
            await self.session.message.edit(content=self.get_content())
        except Exception as e:
            await self.session.bot.on_command_error(self.session.context, e)
        await self.end_game()

    async def on_reaction(self, reaction, user):
        raise NotImplementedError

    async def end_game(self):
        try:
            await self.session.message.clear_reactions()
            if self.session.message_extra is not None:
                await self.session.message_extra.clear_reactions()
        except Exception as e:
            await self.session.bot.on_command_error(self.session.context, e)

        self.emojis = set()

        for winner in self.winners:
            self.session.stats_players[winner.id]["wins"] += 1
        for loser in self.losers:
            self.session.stats_players[loser.id]["losses"] += 1
        for drawer in self.drawers:
            self.session.stats_players[drawer.id]["draws"] += 1

        await self.session.pause()
