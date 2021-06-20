from abc import ABC, abstractmethod


class DiscordMinigame(ABC):
    @abstractmethod
    async def start_game(self): pass

    @abstractmethod
    async def end_game(self): pass

    @abstractmethod
    async def on_player_timed_out(self): pass

    @abstractmethod
    def on_start_move(self): pass

    @abstractmethod
    def on_end_move(self): pass

    @abstractmethod
    def get_board(self): pass

    @abstractmethod
    def update_last_seen(self): pass

    @abstractmethod
    def clear_reactions(self): pass
