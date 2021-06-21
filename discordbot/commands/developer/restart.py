import asyncio
import time

from discordbot.categories.developer import Developer
from discordbot.commands.command import Command
from discordbot.utils.emojis import NUMBERS
from discordbot.utils.private import DISCORD


class RestartCommand(Command):
    name: str = "restart"
    help: str = "Restarts this bot. The Restarter:tm:, *smort* or f o r c e  restarts."
    brief: str = "The Restarter:tm:, *smort* or f o r c e  restarts."
    args: str = ""
    category: str = Developer

    @classmethod
    async def invoke(cls, context):
        if not cls.has_permission(context.message.author.id):
            return

        if cls.bot.game_manager.has_open_sessions():
            await cls.smart_restart(context)

        try:
            await cls.bot.on_restart()
            await context.send(f"Restarting...")
        except Exception as e:
            print(e)
        await cls.bot.close()

    @classmethod
    async def smart_restart(cls, context):
        msg = await context.send(f"There are open sessions, are you sure?\n"
                                 f"{NUMBERS[1]}: **force restart**\n"
                                 f"{NUMBERS[2]}: **smart restart**\n")
        await msg.add_reaction(NUMBERS[1])
        await msg.add_reaction(NUMBERS[2])

        def check(r, u):
            return r.message.id == msg.id and u.id in DISCORD["DEVS"]

        try:
            reaction, user = await cls.bot.wait_for("reaction_add", check=check, timeout=60.0)
        except TimeoutError:
            return
        if reaction.emoji == NUMBERS[1]:
            await context.send(f"Force restarting...")
            return

        elif reaction.emoji == NUMBERS[2]:
            await context.send(f"Smart restarting...")
            cls.bot.game_manager.on_pending_update()
            start_time = time.time()
            while cls.bot.game_manager.has_open_sessions() and time.time() - start_time < 60 * 10:
                await asyncio.sleep(10)
            return

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
