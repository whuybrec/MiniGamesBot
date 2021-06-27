import asyncio
from asyncio import FIRST_COMPLETED

import discord_components


class ButtonManager:
    def __init__(self, bot):
        self.bot = bot
        self.pools = dict()

    def add_buttons(self, checks, handlers):
        tasks = []
        for check in checks:
            tasks.append(asyncio.create_task(self.bot.wait_for("button_click", check=check)))

        ButtonPool(self, tasks)


class ButtonPool:
    def __init__(self, manager, tasks):
        self.manager = manager
        self.tasks = tasks

    def add_to_pool(self, tasks):
        self.tasks.append(*tasks)

    async def start(self):
        done, pending = await asyncio.wait(self.tasks, return_when=FIRST_COMPLETED)
        interaction: discord_components.Interaction = done[0]
        # dict[clicked_button_id](interaction)
