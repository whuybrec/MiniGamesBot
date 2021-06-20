import asyncio


class GameManager:
    def __init__(self):
        self.sessions = list()

    async def on_bot_restart(self):
        for session in self.sessions:
            await session.on_bot_restart()

    def has_open_sessions(self):
        return len(self.sessions) > 0

    async def start_session(self, session):
        self.sessions.append(session)
        await session.start_game()

    def close_session(self, session):
        self.sessions.remove(session)

    def on_pending_update(self):
        for session in self.sessions:
            session.on_pending_update()

    async def close_inactive_sessions(self):
        while True:
            for session in self.sessions:
                if await session.is_inactive():
                    await session.close()
                    self.close_session(session)
            await asyncio.sleep(60 * 5)
