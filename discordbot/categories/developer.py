from .category import Category
from discordbot.private import DISCORD


class Developer(Category):
    name = "developer"

    @classmethod
    def has_permission(cls, user_id):
        if user_id in DISCORD["DEVS"]:
            return True
        return False
