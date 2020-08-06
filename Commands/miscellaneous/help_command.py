from Commands.discord_command import DiscordCommand
from Other.variables import Variables
from Other.private import Private

class HelpCommand(DiscordCommand):
    bot = None
    name = "help"
    help = "Displays the help message with a list of all commands."
    brief = "Gives this message."
    usage = ""
    category = "miscellaneous"

    @classmethod
    async def handler(cls, context, *args, **kwargs):
        if args:
            await cls.extended_help(context, args[0])
            return

        prefix = cls.bot.prefix
        if str(context.channel.guild.id) in Private.prefixes.keys():
            prefix = Private.prefixes[str(context.channel.guild.id)]

        text = "```fix\n" \
               "MINIGAMESBOT``````diff\n" \
               "- minigames\n"
        for command in cls.bot.my_commands:
            if command.category == "minigame":
                text += "\t{0}\n".format(prefix+command.name + " " + command.usage)
        text += "``````diff\n" \
                "- miscellaneous\n"
        for command in cls.bot.my_commands:
            if command.category == "miscellaneous":
                text += "\t{0:30} | {1}\n".format(prefix+command.name + " " + command.usage, command.brief)
        text += "``````ini\n\nType \"" + prefix + "help [command]\" to see more info about that command.\n"
        text += Variables.EXTRA
        text += "```"
        await context.message.channel.send(text)

    @classmethod
    async def extended_help(cls, context, arg):
        prefix = cls.bot.prefix
        if str(context.channel.guild.id) in Private.prefixes.keys():
            prefix = Private.prefixes[str(context.channel.guild.id)]

        called_command = context.message.content[len(cls.bot.prefix + "help "):]
        for command in cls.bot.my_commands:
            if command.name == called_command:
                text = "```diff\n"
                text += "{0}\n\n".format(prefix + "help " + arg)
                text += "+ {0}:\n\t\t{1}\n".format(command.name, command.brief)
                text += "+ {0}:\n\t\t{1} {2}\n".format("Usage", prefix + command.name, command.usage)
                text += "+ {0}:\n\t\t{1}\n".format("Description", "\n        ".join(command.help.split("\n")))
                text += "```"
                await context.message.channel.send(text)
                return
