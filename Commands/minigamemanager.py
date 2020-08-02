from Minigames.blackjack import BlackJack
from Minigames.connect4 import Connect4
from Minigames.guessword import GuessWord
from Minigames.hangman import HangMan
from Minigames.scramble import Scramble
from Minigames.quizmaster import QuizMaster
from Minigames.uno import Uno
from Minigames.chess.chess import Chess
from Other.variables import Variables, increment_game


class MiniGameManager:
    def __init__(self, bot):
        self.bot = bot
        self.open_games = dict()  # {msgID: GameObject}
        self.open_chess_games = dict()  # {serverID: GameObject}
        self.minigames = {"blackjack": BlackJack,
                          "guessword": GuessWord,
                          "hangman": HangMan,
                          "connect4": Connect4,
                          "scramble": Scramble,
                          "quiz": QuizMaster,
                          "uno": Uno,
                          "chess": Chess
                          }
        self.restarting = False

    async def add_game(self, context, game_name, *args):
        if self.restarting:
            return
        msg = await context.channel.send("Starting a game of " + game_name + " ...")
        if game_name == "chess":
            if not context.channel.id in self.open_chess_games.keys():
                self.open_chess_games[context.channel.id] = self.minigames[game_name](self, msg, *args)
                await self.open_chess_games[context.channel.id].start_game()
            else:
                await msg.edit(content="There can only be one open chess game per channel. "
                                       "Finish the previous one before starting a new one or "
                                       "consider going to a different channel.")
        else:
            self.open_games[msg.id] = self.minigames[game_name](self, msg, *args)
            await self.open_games[msg.id].start_game()
        increment_game(game_name)

    async def close_game(self, msg, game=None):
        if game is not None:
            if game == "chess":
                del self.open_chess_games[msg.channel.id]
                return
        del self.open_games[msg.id]

    async def force_close_all(self):
        self.restarting = True
        for game in self.open_games.values():
            game.force_quit()
        self.open_games = dict()

    async def update_game(self, reaction, user):
        for game in self.open_games.values():
            if isinstance(game, Uno):
                if reaction.message.id in game.dms:
                    game.reschedule()
                    await game.update_game(reaction, user)
                    return
        try:
            await self.open_games[reaction.message.id].update_game(reaction, user)
        except:
            pass

    async def dm_update(self, message):
        for game in self.open_games.values():
            if isinstance(game, Uno):
                user = self.bot.get_user(message.author.id)
                for player in game.players:
                    if user.name == player.name:
                        game.reschedule()
                        await game.update_chat(message)

    async def channel_update(self, message):
        if message.channel.id in self.open_chess_games.keys():
            import re
            if re.match(r"^\D\d to \D\d$", message.content):
                game = self.open_chess_games[message.channel.id]
                game.reschedule()
                await game.update_game(message.content.lower(), message.author)
