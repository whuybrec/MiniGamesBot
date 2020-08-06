class DiscordCommand:
    bot = None
    name = "CommandName"
    help = "CommandHelp"
    brief = "CommandBrief"
    usage = "CommandUsage"
    category = "CommandCategory"

    @classmethod
    def add_command(cls, bot):
        cls.bot = bot
        cls.bot.remove_command(cls.name)
        cls.bot.command(name=cls.name, brief=cls.brief, usage=cls.usage)(cls.handler)

    @classmethod
    def handler(cls, context, *args, **kwargs):
        pass
