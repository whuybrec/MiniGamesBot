import sys
import time
import traceback
import discord
import discord.client
from discord.ext.commands import Bot, Cog, CommandNotFound
from discord.utils import find
from Commands.miscellaneous import help_command, info_command, set_prefix_command, bug_command, request_command
from Commands.minigames import blackjack_command, chess_command, connect4_command, quiz_command, hangman_command, \
    scramble_command, uno_command, guessword_command
from Commands.developer import delete_command, say_command, temperature_command, drill_command
from Minigames.minigamemanager import MiniGameManager
from Other.private import Private
from Other.statistics import Statistics
from Other.variables import on_startup
import asyncio

ctx = None
_self = None

class MiniGamesBot(Bot):
    def __init__(self, prefix):
        self.prefix = prefix
        super().__init__(command_prefix=self.prefix)
        self.stats = Statistics(self)
        self.game_manager = MiniGameManager(self)
        self.on_startup()
        self.called = False

        self.my_commands = [help_command.HelpCommand, blackjack_command.BlackjackCommand, chess_command.ChessCommand,
                            connect4_command.Connect4Command, hangman_command.HangmanCommand, quiz_command.QuizCommand,
                            guessword_command.GuesswordCommand, scramble_command.ScrambleCommand, uno_command.UnoCommand,
                            delete_command.DeleteCommand, say_command.SayCommand, temperature_command.TemperatureCommand,
                            drill_command.DrillCommand, info_command.InfoCommand, set_prefix_command.SetPrefixCommand,
                            bug_command.BugCommand, request_command.RequestCommand]
        for command in self.my_commands:
            command.add_command(self)

        self.command(name="exec", brief="<dev> exec belleketrek")(self.execute)
        self.command(name="exit", brief="<dev> Reboots connect4")(self.reboot)
        self.command(name="stats", brief="<dev> gives the daily stats")(self.stats.update_stats)
        self.command(name="renewstats", brief="<dev> resets the stats")(self.stats.renew)

    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
            if message.author.bot:
                return
            await self.game_manager.dm_update(message)
            return

        # command handling
        if str(message.channel.guild.id) in Private.prefixes.keys():
            if message.content.startswith(Private.prefixes[str(message.channel.guild.id)]):
                message.content = self.prefix + message.content[len(Private.prefixes[str(message.channel.guild.id)]):]
            else:
                return

        ctxt = await self.get_context(message)
        await self.invoke(ctxt)

    async def on_guild_join(self, guild):
        general = find(lambda x: 'general' in x.name, guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send('Hello {}! The command prefix for this bot is "?".\n'
                               'Type ?help for a list of commands.'.format(guild.name))

    async def on_reaction_add(self, reaction, user):
        await self.game_manager.update_game(reaction, user)

    def on_startup(self):
        print("Getting data...")
        on_startup()
        print("Done!")

    async def on_ready(self):
        if not self.called:
            self.called = True
            channel = self.get_channel(Private.PRIM_CHANNELID)
            await channel.send("READY.")

    async def reboot(self, context):
        if context.author.id in Private.DEV_IDS.keys():
            await context.send("Saving statistics...")
            self.stats.write_var()
            await context.send("Closing all games...")
            await self.game_manager.force_close_all()
            await context.send("Rebooting...")
            try:
                await self.close()
            except:
                pass
            await self.logout()

    async def on_error(self, event_method, *args, **kwargs):
        e = sys.exc_info()
        if e[0] is discord.Forbidden:
            context = await self.get_context(args[0].message)
            await context.channel.send("I am missing permissions in this server, "
                                       "make sure that I can manage messages (to delete reactions) and can send DMs.")
        text = "```\n\n" \
               "Time: {0}\n\n" \
               "Ignoring exception in command {1}:\n\n" \
               "args: {2}\n\n" \
               "kwargs: {3}\n\n" \
               "e: {4}\n\n" \
               "```".format(time.strftime("%b %d %Y %H:%M:%S"), event_method, args, kwargs, e)
        channel = self.get_channel(Private.LOGS_COMMANDS_CHANNELID)
        await channel.send(text)

    async def on_command_error(self, context, exception):
        """The command error handler provided by the bot."""
        if isinstance(exception, CommandNotFound):
            return
        if self.extra_events.get('on_command_error', None):
            return
        if hasattr(context.command, 'on_error'):
            return

        cog = context.cog
        if cog:
            if Cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        if isinstance(exception, discord.Forbidden):
            await context.channel.send("I am missing permissions in this server, "
                                       "make sure that I can manage messages (to delete reactions) and can send DMs.")

        text = "```\n\n" \
               "Time: {0}\n\n" \
               "Ignoring exception in command {1}:\n\n" \
               "Exception: {2}\n\n" \
               "```".format(time.strftime("%b %d %Y %H:%M:%S"), context.command, exception)
        channel = self.get_channel(Private.LOGS_COMMANDS_CHANNELID)
        await channel.send(text)
        result = traceback.format_exception(type(exception), exception, exception.__traceback__)
        result = "".join(result)
        if len(result) > 1800:
            i = 0
            s = len(result)
            while s > 1800:
                try:
                    await channel.send("```" + result[1800*i:1800*(i+1)] + "```")
                    i += 1
                except discord.errors.HTTPException:
                    await channel.send("```" + result[1800*i:] + "```")
                s -= 18000
        else:
            await channel.send("```"+result+"```")

    async def execute(self, context):
        global ctx, _self
        ctx = context
        _self = self
        if context.message.author.id == Private.DEVALPHA_ID:
            lines = context.message.content[len("?exec "):].split("\n")
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
                await context.send("```python\n" + str(e) + "\n```")
