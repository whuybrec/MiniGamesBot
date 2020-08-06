from Commands.discord_command import DiscordCommand
from Other.private import Private
import json

class SetPrefixCommand(DiscordCommand):
    bot = None
    name = "set_prefix"
    help = "Admins can use this command to set a different prefix for the MiniGamesBot."
    brief = "<admin> set a new prefix for minigamesbot in this server."
    usage = "[new_prefix]"
    category = "miscellaneous"

    @classmethod
    async def handler(cls, context, *args: str, **kwargs):
        if not args or len(args) > 1:
            return

        if not context.channel.permissions_for(context.author).administrator:
            await context.channel.send("Invalid command: only admins can change the prefix.")
            return

        prefix = args[0]

        if len(prefix) > 15:
            await context.channel.send("Invalid prefix: prefix can not be larger than 15 characters.")
            return

        Private.prefixes[str(context.guild.id)] = prefix
        await context.channel.send("The prefix of minigamesbot is now set to '" + prefix + "'")

    def add_new_prefix(self):
        f = open('Data/prefixes.json', 'w')
        tmp = json.dumps(Private.prefixes)
        f.write(tmp)
        f.close()

