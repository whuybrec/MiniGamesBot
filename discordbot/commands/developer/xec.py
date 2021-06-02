import asyncio

from discordbot.categories.developer import Developer
from discordbot.commands.command import Command
from discordbot.utils.private import DISCORD

ctx = None
bot = None


class ExecuteCommand(Command):

    name: str = "exec"
    help: str = "Execute python code."
    brief: str = "Exec snek"
    args: str = "snek code"
    category: str = Developer

    @classmethod
    async def handler(cls, context):
        if not cls.has_permission(context.message.author.id):
            return

        global bot, ctx
        bot = cls.bot
        ctx = context

        lines = context.message.content[len(cls.bot.prefix + cls.name) + 1:].split("\n")
        func = ["async def get():",
                "    try:",
                "        global returnv",
                "        returnv = None",
                "        returnv = await func()",
                "        if returnv is not None:",
                "            await ctx.send(f'```python\\n{repr(returnv)}\\n```')",
                "    except Exception as e:",
                "        await ctx.send(f'```python\\n{e}\\n```')",
                "asyncio.Task(get())",
                "async def func():",
                "    " + "\n    ".join(lines[:-1])]

        keywords = ["return ",
                    "import ",
                    "from ",
                    "for ",
                    "with ",
                    "def ",
                    "else "]

        if lines[-1].startswith(" ") or lines[-1].startswith("\t") or any(
                lines[-1].startswith(s) for s in keywords):
            func.append("    " + lines[-1])
        else:
            func += ["    try:",
                     "        return " + lines[-1],
                     "    except:",
                     "        " + lines[-1]]

        try:
            exec("\n".join(func), globals())
        except Exception as e:
            await ctx.send("```python\n" + str(e) + "\n```")

    @classmethod
    def dummy(cls):
        """this is a dummy method so that the asyncio import doesn't get auto-removed"""
        asyncio.tasks = None

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
