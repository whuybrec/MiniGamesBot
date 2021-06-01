
class Command:
    bot = None
    name = "CommandName"
    help = "CommandHelp"
    brief = "CommandBrief"
    args = "CommandArgs"
    category = "CommandCategory"

    @classmethod
    def add_command(cls, bot):
        cls.bot = bot
        cls.bot.remove_command(cls.name)
        cls.bot.command(name=cls.name, brief=cls.brief, usage=cls.args)(cls.handler)

    @classmethod
    async def handler(cls, context):
        pass

    @classmethod
    def has_permission(cls, user_id):
        return True

