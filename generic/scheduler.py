import asyncio
from time import time


class Scheduler:
    max_wait = 10 * 60  # in seconds
    store_metadata = False

    def __init__(self):
        self.events = dict()  # {scheduler_key: (time, function, args, kwargs, metadata), ...}
        self.waiters = set()  # {t1, t2, t3, ...}

    # interface methods

    def add(self, delay, function, *args, **kwargs):
        """Schedule an event in a specific amount of time."""
        return self.at(time() + delay, function, *args, **kwargs)

    def at(self, t, function, *args, **kwargs):
        """Schedule an event at a specific timestamp ``t``."""
        now = time()
        t = max(now, t)

        if Scheduler.store_metadata and "metadata" in kwargs:
            metadata = kwargs["metadata"]
            del kwargs["metadata"]
        else:
            metadata = None

        key = object()
        self.events[key] = (t, function, args, kwargs, metadata)
        asyncio.Task(self._create_waiter(t, now))

        return key

    def cancel(self, key):
        """Cancel a scheduled event."""
        if key in self.events:
            del self.events[key]

    def is_done(self, key):
        """Return whether a scheduled event has finished."""
        return key not in self.events

    def size(self):
        """Return the amount of events scheduled."""
        return len(self.events)

    # internal methods

    async def _create_waiter(self, t, now=None):
        """Make sure there is a waiter that triggers before timestamp ``t``."""
        if now is None:
            now = time()

        # there is already another waiter before ``t``, which will create a waiter on its own once triggered
        if any(waiter <= t for waiter in self.waiters):
            return

        # never wait more than max_wait to prevent long sleeps
        t = min(t, now + Scheduler.max_wait)

        # start waiter
        self.waiters.add(t)
        asyncio.Task(self._wait(t, now))

    async def _wait(self, t, now):
        """Wait until timestamp ``now``, _pop(), and create new waiter if any events left."""

        # sleep
        await asyncio.sleep(t - now)
        self.waiters.remove(t)

        # execute events
        await self._pop(t)

        # if there are events left, make sure there is another waiter for the first event
        if len(self.events) > 0:
            t = min(tup[0] for tup in self.events.values())
            await self._create_waiter(t)

    async def _pop(self, now):
        """Execute every event scheduled to run before timestamp ``now``."""

        # collect every event that should be triggered before ``now``
        events = []
        for key in list(self.events.keys()):
            t = self.events[key][0]
            if t <= now:
                events.append(self.events[key])
                del self.events[key]

        # execute each of those events
        for t, function, args, kwargs, metadata in events:
            try:
                if asyncio.iscoroutinefunction(function):
                    await function(*args, **kwargs)
                elif asyncio.iscoroutine(function):
                    await function
                else:
                    function(*args, **kwargs)
            except Exception as e:
                import traceback
                print("[EXCEPTION IN SCHEDULER]")
                print(e)
                print("[TRACEBACK]")
                print(traceback.format_exc())
