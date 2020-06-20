from Minigames.blackjack import BlackJack
from Minigames.connect4 import Connect4
from Minigames.guessword import GuessWord
from Minigames.hangman import HangMan
from Minigames.scramble import Scramble
from Minigames.quizmaster import QuizMaster
from Minigames.uno import Uno
from Other.variables import Variables, increment_game


class MiniGameManager:
    def __init__(self, bot):
        self.bot = bot
        self.open_games = dict() # {msgID: GameObject}
        self.minigames = {"blackjack": BlackJack,
                          "guessword": GuessWord,
                          "hangman": HangMan,
                          "connect4": Connect4,
                          "scramble": Scramble,
                          "quiz": QuizMaster,
                          }
        self.restarting = False

    async def add_game(self, context, game_name, *args):
        if self.restarting: return
        msg = await context.channel.send("Starting a game of " + game_name + " ...")
        self.open_games[msg.id] = self.minigames[game_name](self, msg, *args)
        await self.open_games[msg.id].start_game()
        increment_game(game_name)

    async def close_game(self, msg):
        del self.open_games[msg.id]

    async def force_close_all(self):
        self.restarting = True
        for game in self.open_games.values():
            game.force_quit()
        self.open_games = dict()

    async def update_game(self, reaction, user):
        try:
            game = self.open_games[reaction.message.id]
        except KeyError:
            return
        if isinstance(game, Uno):
            if reaction.message.id in game.dms:
                await game.update_game(reaction, user)
        else:
            try:
                await game.update_game(reaction, user)
            except:
                pass

    async def dm_update(self, message):
        for game in self.open_games.values():
            if isinstance(game, Uno):
                user = self.bot.get_user(message.author.id)
                for player in game.players:
                    if user.name == player.name:
                        await game.update_chat(message)
