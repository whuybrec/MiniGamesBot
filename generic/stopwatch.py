import time


class Stopwatch:
    def __init__(self):
        self.start_t = 0
        self.total_t = 0

    def start(self):
        self.start_t = time.time()

    def pause(self):
        self.total_t += time.time() - self.start_t

    def get_total_time(self):
        return self.total_t

    def reset(self):
        self.start_t = 0
        self.total_t = 0
