""" Modul for time-klassen """
import time


class Timer:
    def __init__(self, name="method"):
        self._start_time = time.time_ns()
        self._name = name

    def stop(self):
        """ Stopper tiden og returnerer differensen """
        difference = time.time_ns() - self._start_time
        print(f"Time elapsed doing {self._name}: {difference / 1e9:.2f}s")
        return difference
