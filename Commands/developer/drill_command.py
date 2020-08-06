from Commands.discord_command import DiscordCommand
from Other.private import Private
from Other.variables import Variables

class DrillCommand(DiscordCommand):
    bot = None
    name = "drill"
    help = "The bot starts every minigame."
    brief = "The bot starts every minigame."
    usage = ""
    category = "developer"

    @classmethod
    async def handler(cls, context, *args: str, **kwargs):
        if context.author.id in Private.DEV_IDS.keys():
            for game in Variables.game_names:
                if game == "connect4":
                    await cls.bot.game_manager.add_game(context, game, context.author.id, Private.TEST_ACC_ID)
                elif game == "uno":
                    await cls.bot.game_manager.add_game(context, game, [cls.bot.get_user(context.author.id),
                                                                        cls.bot.get_user(Private.TEST_ACC_ID)])
                elif game == "chess":
                    await cls.bot.game_manager.add_game(context, game, context.author.id, Private.TEST_ACC_ID)
                else:
                    await cls.bot.game_manager.add_game(context, game, context.author.id)