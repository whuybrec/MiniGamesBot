from discordbot.messagemanager import MessageManager
from discordbot.user.discord_games import *
from discordbot.user.session import Session


class GameManager:
    bot = None
    scheduler = None
    open_sessions = list()

    minigames = {
        "scramble": ScrambleDiscord,
        "quiz": QuizDiscord,
        "mastermind": MastermindDiscord,
        "hangman": HangmanDiscord,
        "flood": FloodDiscord,
        "blackjack": BlackjackDiscord,
        "akinator": AkinatorDiscord,
        "chess": ChessDiscord,
        "connect4": Connect4Discord
    }

    @classmethod
    def on_startup(cls, bot):
        cls.bot = bot
        cls.scheduler = cls.bot.scheduler

    @classmethod
    async def on_bot_restart(cls):
        for session in cls.open_sessions:
            await session.on_bot_restart()

    @classmethod
    def has_open_sessions(cls):
        return len(cls.open_sessions) > 0

    @classmethod
    async def create_session(cls, message, minigame, *players):
        session = Session(cls, message, minigame, *players)
        await cls.start_session(session)

    @classmethod
    async def start_session(cls, session):
        if cls.bot.has_update:
            await MessageManager.edit_message(session.message, "Sorry! I can't start any new games right now. Boss says I have to restart soon:tm:. Try again later!")
            return

        cls.open_sessions.append(session)
        await session.start()

    @classmethod
    def close_session(cls, session):
        cls.open_sessions.remove(session)

    @classmethod
    def add_player_stats_to_db(cls, player_id, minigame, games_played, wins, losses, draws, time, is_idle):
        cls.bot.db.add_to_players_table(player_id, minigame, games_played, wins, losses, draws, time, is_idle)

    @classmethod
    def add_minigame_stats_to_db(cls, server_id, minigame, games_played, wins, losses, draws, time, timeout):
        cls.bot.db.add_to_minigames_table(server_id, minigame, games_played, wins, losses, draws, time, timeout)
