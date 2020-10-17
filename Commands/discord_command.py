import time

from Database.database import DataBase

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
        cls.bot.command(name=cls.name, brief=cls.brief, usage=cls.usage)(cls.inc_command_counter)

    @classmethod
    async def inc_command_counter(cls, context, *args):
        date = time.strftime("%Y-%m-%d")
        row = DataBase.run("""SELECT amount FROM commands WHERE command='{0}' AND date_='{1}'""".format(cls.name, date))
        if row:
            amt = row[0][0]
            amt += 1
            DataBase.run("""UPDATE commands SET amount={0} WHERE command='{1}' AND date_='{2}'""".format(amt, cls.name, date))
        else:
            DataBase.run("""INSERT INTO commands(date_, command, amount) VALUES ('{0}', '{1}', {2})""".format(date, cls.name, 1))

        await cls.handler(context, *args)

    @classmethod
    async def handler(cls, context, *args):
        pass

    @classmethod
    async def illegal_command(cls, context):
        await context.message.channel.send("Invalid command to start minigame, check the help message for more info")
        return
