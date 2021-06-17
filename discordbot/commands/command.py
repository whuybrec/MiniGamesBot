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
        missing_permissions = cls.bot.get_missing_permissions(context)
        if len(missing_permissions) > 0:
            await cls.bot.send_missing_permissions(context, missing_permissions)
            return

        await cls.invoke(context)

    @classmethod
    async def invoke(cls, context):
        pass

    @classmethod
    def has_permission(cls, user_id):
        return True
