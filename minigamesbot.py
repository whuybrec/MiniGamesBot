import json
import re
import time
import traceback

import discord
import discord.client
from discord.ext.commands import Bot, Cog, CommandNotFound
from discord.utils import find

import Commands.devcommands
from Commands.minigamemanager import MiniGameManager
from Other.private import Private
from Other.statistics import Statistics
from Other.variables import Variables, on_startup
import asyncio

ctx = None
_self = None

class MiniGamesBot(Bot):
    def __init__(self, prefix):
        self.prefix = prefix
        self.stats = Statistics(self)
        self.game_manager = MiniGameManager(self)
        self.on_startup()
        self.called = False

        super().__init__(command_prefix=self.prefix)
        self.remove_command("help")
        self.command(name="exit", brief="<dev> Reboots connect4")(self.shut_down)
        self.command(name="say", brief="[args] | <dev> ConnectBot says the arg")(Commands.devcommands.say)
        self.command(name="del", brief="[msgID] | <dev> Delete the message from id")(Commands.devcommands.delete)
        self.command(name="stats", brief="<dev> gives the daily stats")(self.stats.update_stats)
        self.command(name="renewstats", brief="<dev> resets the stats")(self.stats.renew)
        self.command(name="temp", brief="<dev> gets temp of RPI")(Commands.devcommands.temp)
        self.command(name="exec", brief="<dev> exec belleketrek")(self.execbelleketrek)
        self.command(name="drill", brief="<dev> do the drill bot")(self.drill)
        self.devcmdsstr = ["exit", "say", "del", "servers", "stats", "temp", "drill"]
        self.devcmds = []

        self.command(name="help", brief="Gives this message", help="Gives a list of all commands")(self.help)
        self.command(name="info", brief="Displays some information about the bot",
                     help="Gives a short message from the developper")(self.info)
        self.command(name="set_prefix", usage="\"[new prefix]\"",
                     brief="\"new prefix\" | <admin> sets a new prefix for minigamesbot in this server.",
                     help="Admins can use this command to set a different prefix to minigamesbot")(self.set_prefix)
        self.command(name="bug", usage="[bug description]",
                     brief="Let the dev know you found a bug by giving detailed information as the argument.",
                     help="Let the dev know you found a bug by giving detailed information so it can be resolved."
                          "\nInformation that is required: game, last action, status of the game "
                          "(picture or discription)")(self.bug)
        self.command(name="request", usage="[request description]",
                     brief="You have an idea for a new minigame or for an existing minigame "
                           "and you would like to let the dev know.",
                     help="You have an idea for a new minigame or for an existing minigame "
                          "and you would like to let the dev know. "
                          "Give a discription as argument to the command.")(self.request)
        self.othercmdsstr = ["help", "info", "set_prefix", "bug", "request"]
        self.othercmds = []

        self.command(name="blackjack", brief="Start a game of blackjack",
                     help=Variables.BJRULES)(self.blackjack_game)
        self.command(name="connect4", brief="Start a game of connect4", usage="[@player2]",
                     help=Variables.C4RULES)(self.connect4_game)
        self.command(name="hangman", brief="Start a game of hangman",
                     help=Variables.HMRULES)(self.hangman_game)
        self.command(name="scramble", brief="Start a game of scramble",
                     help=Variables.SCRULES)(self.scramble_game)
        self.command(name="guessword", brief="Start a game of guessword",
                     help=Variables.GWRULES)(self.guessword_game)
        self.command(name="quiz", brief="Start a quiz",
                     help=Variables.QZRULES)(self.quiz_game)
        self.command(name="uno", brief="Start a game of uno",  usage="[@player1] ... [@player10]",
                     help=Variables.UNORULES)(self.uno_game)
        self.command(name="chess", brief="Start a game of chess", usage="[@player2]",
                     help=Variables.CHESSRULES)(self.chess_game)
        self.minigamescmds = []

        for command in self.commands:
            if command.name in self.devcmdsstr:
                self.devcmds.append(command)
            elif command.name in self.othercmdsstr:
                self.othercmds.append(command)
            elif command.name in Variables.game_names:
                self.minigamescmds.append(command)

    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
            if message.author.bot: return
            await self.game_manager.dm_update(message)
            return

        # command handling
        if str(message.channel.guild.id) in Private.prefixes.keys():
            if message.content.startswith(Private.prefixes[str(message.channel.guild.id)]):
                message.content = self.prefix+message.content[len(Private.prefixes[str(message.channel.guild.id)]):]
            else:
                return

        await self.game_manager.channel_update(message)

        ctxt = await self.get_context(message)
        await self.invoke(ctxt)

    async def on_guild_join(self, guild):
        general = find(lambda x: 'general' in x.name, guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send('Hello {}! The command prefix for this bot is "?"\nType ?help for a list of commands'.format(guild.name))

    async def on_reaction_add(self, reaction, user):
        await self.game_manager.update_game(reaction, user)

    async def set_prefix(self, context, prefix):
        if not context.channel.permissions_for(context.author).administrator:
            await context.channel.send("Invalid command: only admins can change the prefix.")
            return

        if len(prefix) > 15:
            await context.channel.send("Invalid prefix: prefix can not be larger than 15 characters.")
            return

        Private.prefixes[str(context.guild.id)] = prefix
        f = open('Data/prefixes.json', 'w')
        tmp = json.dumps(Private.prefixes)
        f.write(tmp)
        f.close()
        await context.channel.send("The prefix of minigamesbot is now set to '" + prefix + "'")

    async def blackjack_game(self, context):
        await self.game_manager.add_game(context, "blackjack", context.author.id)

    def on_startup(self):
        print("Getting data...")
        on_startup()
        print("Done!")

    async def on_ready(self):
        if not self.called:
            self.called = True
            channel = self.get_channel(Private.PRIM_CHANNELID)
            await channel.send("READY.")

    async def connect4_game(self, context, p2):
        players = [context.author.id]
        temp = re.findall(r'\d+', p2)
        try:
            pid = int(list(map(int, temp))[0])
            if pid == players[0]:
                await context.message.channel.send("Invalid command: tag unique players to start connect4 game.")
                return
            players.append(pid)
        except:
            await context.message.channel.send("Invalid command: tag unique players to start connect4 game.")
        await self.game_manager.add_game(context, "connect4", players[0], players[1])

    async def chess_game(self, context, p2):
        players = [context.author.id]
        temp = re.findall(r'\d+', p2)
        try:
            pid = int(list(map(int, temp))[0])
            if pid == players[0]:
                await context.message.channel.send("Invalid command: tag unique players to start chess game.")
                return
            players.append(pid)
        except:
            await context.message.channel.send("Invalid command: tag unique players to start chess game.")
        await self.game_manager.add_game(context, "chess", players[0], players[1])

    async def scramble_game(self, context):
        await self.game_manager.add_game(context, "scramble", context.author.id)

    async def hangman_game(self, context):
        await self.game_manager.add_game(context, "hangman", context.author.id)

    async def guessword_game(self, context):
        await self.game_manager.add_game(context, "guessword", context.author.id)

    async def quiz_game(self, context):
        await self.game_manager.add_game(context, "quiz", context.author.id)

    async def uno_game(self, context, *args):
        players = list()
        player_names = set()
        for arg in args:
            temp = re.findall(r'\d+', arg)
            try:
                pid = int(list(map(int, temp))[0])
                player = self.get_user(pid)
                players.append(player)
                player_names.add(player.name)
                if len(player_names) != len(players):
                    await context.message.channel.send("Invalid command: tag unique players to start uno game.")
                    return
            except:
                await context.message.channel.send("Invalid command: tag unique players to start uno game.")
                return

        if not 1 < len(players) < 11:
            await context.message.channel.send("Invalid amount of players: minimum of 2 and maximum of 10 players allowed.")
            return
        await self.game_manager.add_game(context, "uno", players)

    async def drill(self, context):
        if context.author.id in Private.DEV_IDS.keys():
            for game in Variables.game_names:
                if game == "connect4":
                    await self.game_manager.add_game(context, game, context.author.id, Private.TEST_ACC_ID)
                elif game == "uno":
                    await self.game_manager.add_game(context, game, [self.get_user(context.author.id), self.get_user(Private.TEST_ACC_ID)])
                elif game == "chess":
                    await self.game_manager.add_game(context, game, context.author.id, Private.TEST_ACC_ID)
                else:
                    await self.game_manager.add_game(context, game, context.author.id)

    async def info(self, context):
        text = "- Check out my github page with the source code, you can sponsor me there too.\n"
        text += "- If you notice any bugs or have any suggestions, make a new issue on my github page or tell me with the bug command!\n"
        text += "- Don't forget to give the bot permissions to manage reactions and messages.\n"
        text += "- Press " + Variables.STOP_EMOJI + " to close the game.\n"
        text += "- Every minigame has a time limit of " + str(int(Variables.DEADLINE/60)) + " minutes.\n"
        text += "- You can find the invite link to this bot on this page: <https://top.gg/bot/704677903182594119>\n"
        text += "- If you wish to make a donation: https://www.buymeacoffee.com/whuybrec\n"
        text += "- Github link: <https://github.com/whuybrec/whuybrec.github.io>\n"
        await context.message.channel.send(text)

    async def shut_down(self, context):
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

    async def bug(self, context):
        channel = self.get_channel(Private.USER_REPORTS_CHANNELID)
        try:
            picture = context.message.attachments[0].url
            await channel.send(picture)
            await channel.send(context.author.name +": " + context.message.content)
        except:
            await channel.send(context.author.name +": " + context.message.content)
        await context.channel.send("Bug succesfully reported!")

    async def request(self, context):
        channel = self.get_channel(Private.USER_REPORTS_CHANNELID)
        await channel.send(context.author.name + ": " + context.message.content)
        await context.channel.send("Request succesfully delivered!")

    async def on_command_error(self, context, exception):
        """|coro|
                The default command error handler provided by the bot.

                By default this prints to :data:`sys.stderr` however it could be
                overridden to have a different implementation.

                This only fires if you do not specify any listeners for command error.
                """
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
            l = len(result)
            while l > 1800:
                try:
                    await channel.send("```" + result[1800*i:1800*(i+1)] + "```")
                    i += 1
                except:
                    await channel.send("```" + result[1800*i:] + "```")
                l -= 18000
        else:
            await channel.send("```"+result+"```")

    async def help(self, context):
        if str(context.channel.guild.id) in Private.prefixes.keys():
            prefix = Private.prefixes[str(context.channel.guild.id)]
        else:
            prefix = self.prefix
        if context.message.content == self.prefix+"help":
            text = "```diff\n"
            text += "- MINIGAMESBOT\n"
            text += "\n+ minigames"
            for command in self.minigamescmds:
                if command.usage is not None:
                    text += "\n   {0} {1}\n\t\t{2}".format("- " + prefix + str(command.name), str(command.usage), str(command.brief))
                else:
                    text += "\n   {0} \n\t\t{1}".format("- " + prefix + str(command.name), str(command.brief))
            text += "\n+ other"
            for command in self.othercmds:
                text += "\n   {0} \n\t\t{1:70s}".format("- " + prefix + str(command.name), str(command.brief))
            text += "\n\nType \"" + prefix+"help [minigame]\" to see the rules of that minigame."
            text += Variables.EXTRA
            text += "\n```"
            await context.message.channel.send(text)
        else:
            called = context.message.content[len(self.prefix+"help "):]
            for command in self.minigamescmds:
                if command.name == called:
                    text = "```diff\n"
                    text += "- " + prefix + called + "\n"
                    if command.usage is not None:
                        text += "\n   + {0}  \n\t\t{1}".format("Arguments", str(command.usage))
                    text += "\n   + {0}  \n\t\t{1}".format("Description", str(command.brief))
                    text += "\n   + {0}  \n{1}".format("Rules", "\t\t" + "\n        ".join(str(command.help).split("\n")))
                    text += "\n```"
                    await context.message.channel.send(text)
                    return

    async def execbelleketrek(self, context):
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
                await context.send("```python\n"+ str(e) + "\n```")

