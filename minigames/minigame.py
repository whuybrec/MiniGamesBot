from abc import ABC, abstractmethod


class Minigame(ABC):
    @abstractmethod
    def has_won(self):
        raise NotImplementedError

    @abstractmethod
    def has_drawn(self):
        raise NotImplementedError

    @abstractmethod
    def has_lost(self):
        raise NotImplementedError
