from Other.private import Private
from Other.variables import Variables, get_next_midnight_stamp
import ast

class Statistics:
    serverCount = 0
    def __init__(self, bot):
        self.bot = bot
        self.msgID = 0

    def get_stats(self):
        total_played = 0
        text = "```css\n{0:15s}\t{1:10s}\n".format("Games", "Today")
        for key, value in Variables.amtPlayedGames.items():
            total_played += int(value)
            text += "{0:15s}\t{1:10s}\n".format(key+':', str(value))
        servers, users = self.get_server_count()
        text += "\nTotal games played: {0}\nServers: {1}\nUsers: {2}".format(total_played, servers, users)
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
            self._write_var()
            if context is None:
                Variables.scheduler.add(60*10, self.update_stats, None)

    """Called every 24 hours"""
    async def renew(self, context):
        if context is None or context.message.author.id == Private.DEVALPHA_ID:
            channel = self.bot.get_channel(Private.STATS_CHANNELID)
            msg = await channel.fetch_message(self.msgID)
            await msg.edit(content=self.get_stats())

            Variables.amtPlayedGames = {Variables.game_names[i]: 0 for i in range(len(Variables.game_names))}
            msg = await channel.send(self.get_stats())
            self.msgID = msg.id
            Variables.scheduler.at(get_next_midnight_stamp(), self.renew, None)

    """Write stats to stats.txt"""
    def _write_var(self):
        f = open('stats.txt', 'w')
        f.write(str(Variables.amtPlayedGames)+"\n")
        f.write(str(self.msgID))
        f.close()

    """Read stats on init"""
    def _read_var(self):
        f = open('stats.txt', 'r')
        content = f.readline()
        dictionary = ast.literal_eval(content)
        Variables.amtPlayedGames = dictionary
        content = f.readline()
        if content != "":
            self.msgID = int(content)
        f.close()

    def get_server_count(self):
        count_s = 0
        count_u = set()
        for guilds in self.bot.guilds:
            if guilds.name != "Discord Bot List":
                count_s += 1
                for u in guilds.members:
                    if not u.bot:
                        count_u.add(u.id)
        return count_s, len(count_u)
