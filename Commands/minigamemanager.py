from Minigames.blackjack import BlackJack
from Minigames.connect4 import Connect4
from Minigames.guessword import GuessWord
from Minigames.hangman import HangMan
from Minigames.scramble import Scramble
from Minigames.quizmaster import QuizMaster
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
                          "quiz": QuizMaster}

    async def add_game(self, context, game_name, *args):
        msg = await context.channel.send("Starting a game of " + game_name + " ...")
        self.open_games[msg.id] = self.minigames[game_name](self, msg, *args)
        await self.open_games[msg.id].start_game()
        Variables.scheduler.add(Variables.DEADLINE, self.force_close, self.open_games[msg.id])
        increment_game(game_name)

    async def close_game(self, msg):
        await msg.clear_reactions()
        del self.open_games[msg.id]

    async def force_close(self, game):
        if game.msg.id in self.open_games.keys():
            await game.msg.edit(content="Game closed, deadline reached.")
            try:
                await game.msg2.delete()
            except:
                pass
            await self.close_game(game.msg)

    async def force_close_all(self):
        for game in self.open_games.values():
            try:
                await game.msg.edit(content="Game closed because the dev is restarting the bot.")
                await game.msg.clear_reactions()
                await game.msg2.delete()
            except:
                pass

    async def update_game(self, reaction, user):
        if reaction.message.id in self.open_games.keys():
            await self.open_games[reaction.message.id].update_game(reaction, user)
