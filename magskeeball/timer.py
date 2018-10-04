import time

class Timer():

    def __init__(self):
        self.start_time = time.perf_counter()
        self.last_tick_time = time.perf_counter()
        self.ticks = 0

    def tick(self,fps):
        this_time = time.perf_counter()
        while self.last_tick_time + 1/fps > this_time:
            this_time = time.perf_counter()
        self.last_tick_time = this_time
        self.ticks += 1
