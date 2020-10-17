from Commands.discord_command import DiscordCommand
from Database.database import DataBase

class AnnouncementsCommand(DiscordCommand):
    bot = None
    name = "announcements"
    brief = "Toggles receiving announcements about the bot in the channel."
    help = "If you want to receive announcements about the bot in this channel, use this command to enable it.\n" \
           "If this channel was already receiving announcements, than typing this command will disable that feature."
    usage = ""
    category = "miscellaneous"

    @classmethod
    async def handler(cls, context, *args):
        if not context.channel.permissions_for(context.author).administrator:
            await context.channel.send("Illegal command: only admins can toggle the announcements feature.")
            return

        channels = DataBase.run("SELECT channel_id "
                                "FROM announcement_channels "
                                "WHERE channel_id={0}"
                                .format(context.channel.id))
        if len(channels) == 0:
            DataBase.run("INSERT INTO announcement_channels(server_id, channel_id) "
                         "VALUES ({0}, {1})"
                         .format(context.message.guild.id, context.channel.id))
            await context.channel.send("This channel will now receive announcements about me!")
        else:
            DataBase.run("DELETE FROM announcement_channels "
                         "WHERE server_id = {0} AND channel_id = {1}"
                         .format(context.message.guild.id, context.channel.id))
            await context.channel.send("Disabled MiniGamesBot announcements in this channel.")