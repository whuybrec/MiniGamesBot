from discord.ext.commands import Bot
from discord.utils import find
from Commands.minigamemanager import MiniGameManager
from Other.private import Private
from Other.variables import Variables, on_startup
from Other.statistics import Statistics
import Commands.devcommands
import discord
import re
import time
import asyncio

ctx = None
_self = None

class MiniGamesBot(Bot):
    def __init__(self, prefix):
        self.called = False
        self.prefix = prefix
        self.stats = Statistics(self)
        self.game_manager = MiniGameManager(self)

        super().__init__(command_prefix=self.prefix)
        self.remove_command("help")
        self.command(name="exit", brief="<dev> Reboots connect4")(self.shut_down)
        self.command(name="say", brief="[args] | <dev> ConnectBot says the arg")(Commands.devcommands.say)
        self.command(name="del", brief="[msgID] | <dev> Delete the message from id")(Commands.devcommands.delete)
        self.command(name="stats", brief="<dev> gives the daily stats")(self.stats.update_stats)
        self.command(name="renewstats", brief="<dev> resets the stats")(self.stats.renew)
        self.command(name="temp", brief="<dev> gets temp of RPI")(Commands.devcommands.temp)
        self.command(name="exec", brief="<dev> exec belleketrek")(self.execbelleketrek)
        self.devcmdsstr = ["exit", "say", "del", "servers", "stats", "temp"]
        self.devcmds = []

        self.command(name="help", brief="Gives this message", help="Gives a list of all commands")(self.help)
        self.command(name="info", brief="Displays some information about the bot", help="Gives a short message from the developper")(self.info)
        self.othercmdsstr = ["help", "info"]
        self.othercmds = []

        self.command(name="blackjack", brief="Start a game of blackjack", help=Variables.BJRULES)(self.blackjack_game)
        self.command(name="connect4", brief="Start a game of connect4", usage="[@player1] [@player2]", help=Variables.C4RULES)(self.connect4_game)
        self.command(name="hangman", brief="Start a game of hangman", help=Variables.HMRULES)(self.hangman_game)
        self.command(name="scramble", brief="Start a game of scramble", help=Variables.SCRULES)(self.scramble_game)
        self.command(name="guessword", brief="Start a game of guessword", help=Variables.GWRULES)(self.guessword_game)
        self.command(name="quiz", brief="Start a quiz", help=Variables.QZRULES)(self.quiz_game)
        self.minigamescmdsstr = ["connect4", "hangman", "scramble", "guessword", "blackjack", "quiz"]
        self.minigamescmds = []

        for command in self.commands:
            if command.name in self.devcmdsstr:
                self.devcmds.append(command)
            elif command.name in self.othercmdsstr:
                self.othercmds.append(command)
            elif command.name in self.minigamescmdsstr:
                self.minigamescmds.append(command)

    async def on_message(self, message):
        # command handling
        ctx = await self.get_context(message)
        await self.invoke(ctx)

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=self.prefix + "help"))
        if not self.called:
            channel = self.get_channel(Private.PRIM_CHANNELID)
            await channel.send("Reading some data...")
            on_startup()
            await channel.send("Getting statistics...")
            await self.stats.on_startup()
            self.called = True
            await channel.send("Ready!")

    async def on_guild_join(self, guild):
        general = find(lambda x: 'general' in x.name, guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send('Hello {}! The command prefix for this bot is "?"\nType ?help for a list of commands'.format(guild.name))

    async def on_reaction_add(self, reaction, user):
        await self.game_manager.update_game(reaction, user)

    async def blackjack_game(self, context):
        await self.game_manager.add_game(context, "blackjack", context.author.id)

    async def connect4_game(self, context, p1, p2):
        try:
            temp = re.findall(r'\d+', p1)
            p1id = int(list(map(int, temp))[0])
            temp = re.findall(r'\d+', p2)
            p2id = int(list(map(int, temp))[0])
            await self.game_manager.add_game(context, "connect4", p1id, p2id)
        except:
            return

    async def scramble_game(self, context):
        await self.game_manager.add_game(context, "scramble", context.author.id)

    async def hangman_game(self, context):
        await self.game_manager.add_game(context, "hangman", context.author.id)

    async def guessword_game(self, context):
        await self.game_manager.add_game(context, "guessword", context.author.id)

    async def quiz_game(self, context):
        await self.game_manager.add_game(context, "quiz", context.author.id)

    async def info(self, context):
        text =  "- Check out my github page with the source code, you can sponsor me there too.\n"
        text += "- If you notice any bugs or have any suggestions, make a new issue on my github page to tell me!\n"
        text += "- Don't forget to give the bot permissions to manage reactions and messages.\n"
        text += "- Press " + Variables.STOP_EMOJI + " to close the game.\n"
        text += "- ?help [minigame] displays more info and the rules of the minigame.\n"
        text += "- Every minigame has a time limit of " + str(int(Variables.DEADLINE/60)) + " minutes.\n"
        text += "- You can find the invite link to this bot on this page: <https://top.gg/bot/704677903182594119>\n"
        text += "- If you wish to make a donation: https://www.buymeacoffee.com/whuybrec\n"
        text += "- Github link: <https://github.com/whuybrec/whuybrec.github.io>\n"
        text += "- My website: <https://whuybrec.github.io/>"
        await context.message.channel.send(text)

    async def shut_down(self, ctx):
        if ctx.author.id in Private.DEV_IDS.keys():
            await ctx.send("Closing all games...")
            await self.game_manager.force_close_all()
            await ctx.send("Saving statisticss...")
            self.stats.write_var()
            await ctx.send("Rebooting...")
            try:
                await self.close()
            except:
                pass
            await self.logout()

    #async def on_error(self, event_method, *args, **kwargs):
    #    channel = self.get_channel(Private.LOGS_CHANNELID)
    #    text = "```\n\n" \
    #           "Time: {0}\n\n" \
    #           "Event: {1}\n\n" \
    #           "Args: {2}\n\n" \
    #           "Kwargs: {3}\n\n" \
    #           "```".format(time.strftime("%b %d %Y %H:%M:%S"),event_method, str(args), str(kwargs))
    #    await channel.send(text)

    async def help(self, context):
        if context.message.content == self.prefix+"help":
            text = "```md\n"
            text +="/* MINIGAMESBOT */\n"
            text +="\n<minigames>"
            for command in self.minigamescmds:
                if command.usage is not None:
                    text += "\n   {0} {1}\n\t\t{2}".format("< " + self.prefix + str(command.name), str(command.usage) + " >", str(command.brief))
                else:
                    text += "\n   {0} \n\t\t{1}".format("< " + self.prefix + str(command.name)+" >", str(command.brief))
            text += "\n<other>"
            for command in self.othercmds:
                text += "\n   {0} \n\t\t{1:70s}".format("< " + self.prefix + str(command.name)+" >", str(command.brief))
            text += "\n\nType " +self.prefix+"help [minigame] to see the rules of that minigame."
            text += Variables.EXTRA
            text += "\n```"
            await context.message.channel.send(text)
        else:
            called = context.message.content[len(self.prefix+"help")+1:]
            for command in self.minigamescmds:
                if command.name == called:
                    text  = "```md\n"
                    text += "/* " + self.prefix + called +" */\n"
                    if command.usage is not None:
                        text += "\n   < {0} > \n\t\t{1}".format("Arguments", str(command.usage))
                    text += "\n   < {0} > \n\t\t{1}".format("Description", str(command.brief))
                    text += "\n   < {0} > \n{1}".format("Rules", "\t\t" + "\n        ".join(str(command.help).split("\n")))
                    text += "\n```"
                    await context.message.channel.send(text)
                    return
            await context.message.channel.send("Illegal command: " + called)

    async def execbelleketrek(self, context):
        if context.message.author.id == Private.DEVALPHA_ID:
            global ctx, _self
            _self = self
            ctx = context
            string = str(context.message.content[len("?exec "):])
            lines = string.split("\n")
            func = ["async def get():",
                    "    global returnv",
                    "    returnv = None",
                    "    returnv = await func()",
                    "    if returnv is not None:",
                    "        await ctx.send(f'```python\\n{repr(returnv)}\\n```')",
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

            if lines[-1].startswith(" ") or lines[-1].startswith("\t") or any(lines[-1].startswith(s) for s in keywords):
                func.append("    " + lines[-1])
            else:
                func += ["    try:",
                         "        return " + lines[-1],
                         "    except:",
                         "        " + lines[-1]]

            try:
                exec("\n".join(func), globals())
            except SyntaxError as e:
                await context.message.channel.send("```" + str(e) + "```")





