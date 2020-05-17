import time
from Other.private import Private
from Other.variables import Variables, get_next_midnight_stamp
import ast
import json
import discord

class Statistics:
    serverCount = 0
    def __init__(self, bot):
        self.bot = bot
        self.msgID = Private.STATS_MSGID

    def get_stats(self):
        total_played = 0
        servers, users = self.get_server_count()

        text = "```md" \
               "\n/* STATISTICS */\n\n"
        text += "{0:10s}   {1}\n".format("<Servers>", str(servers))
        text += "{0:10s}   {1}\n".format("<Users>", str(users))

        text += "\n{0:20s}{1}\n".format("<Games>", "<Usage>")
        for key, value in Variables.amtPlayedGames.items():
            total_played += int(value)
            text += "{0:20s}{1:>4s}\n".format('   < ' + key+' > ', str(value))
        text += "\n{0:20s}{1:>4s}\n\n".format("   < Total >", str(total_played))

        text += "<History>\n"
        for i in range(len(Variables.history)):
            text += "\t{0:5s}   {1}\n".format(Variables.history[i][0], Variables.history[i][1])
        text += "\n{0}: {1}\n".format("Updated", time.strftime("%H:%M:%S"))
        text += "```"
        return text

    async def on_startup(self):
        self._read_var()
        channel = self.bot.get_channel(Private.STATS_CHANNELID)
        if self.msgID == 0:
            msg = await channel.send(self.get_stats())
            self.msgID = msg.id
        else:
            await self.update_stats(None)
        Variables.scheduler.at(get_next_midnight_stamp(), self.renew, None)
        Variables.scheduler.add(60 * 10, self.update_stats, None)

    """Called every 10 minutes"""
    async def update_stats(self, context):
        if context is None or context.message.author.id == Private.DEVALPHA_ID:
            channel = self.bot.get_channel(Private.STATS_CHANNELID)
            try:
                msg = await channel.fetch_message(self.msgID)
                await msg.edit(content = self.get_stats())
            except:
                msg = await channel.send(self.get_stats())
                self.msgID = msg.id
            self.write_var()
            if context is None:
                Variables.scheduler.add(60*10, self.update_stats, None)
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening, name=self.bot.prefix + "help"))

    """Called every 24 hours"""
    async def renew(self, context):
        if context is None or context.message.author.id == Private.DEVALPHA_ID:
            channel = self.bot.get_channel(Private.STATS_CHANNELID)
            msg = await channel.fetch_message(self.msgID)
            await msg.edit(content=self.get_stats())

            total_played = 0
            for key, value in Variables.amtPlayedGames.items():
                total_played += int(value)
            Variables.history.insert(0, [time.strftime("%d/%m"), total_played])
            Variables.amtPlayedGames = {Variables.game_names[i]: 0 for i in range(len(Variables.game_names))}

            self.write_var()
            Variables.scheduler.at(get_next_midnight_stamp(), self.renew, None)

    """Write stats to stats.json"""
    def write_var(self):
        f = open('Data/stats.json', 'w')
        tmp = {"Today": Variables.amtPlayedGames, "History": Variables.history}
        tmp = json.dumps(tmp)
        f.write(tmp)
        f.close()

    """Read stats on init"""
    def _read_var(self):
        json1_file = open('Data/stats.json')
        json1_str = json1_file.read()
        dictionary = json.loads(json1_str)
        json1_file.close()
        Variables.amtPlayedGames = dictionary["Today"]
        Variables.history = dictionary["History"]

    def get_server_count(self):
        count_s = 0
        count_u = set()
        for guilds in self.bot.guilds:
            count_s += 1
            if guilds.name != "Discord Bot List" and guilds.name != "Discord Bots":
                for u in guilds.members:
                    if not u.bot:
                        count_u.add(u.id)
        return count_s, len(count_u)
