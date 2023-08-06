import time
from threading import Thread


class Time:
    __active = True
    timers = []

    @classmethod
    def wait_for_seconds(cls, seconds):
        """Stops a program for 'seconds' seconds.\n
        To stop waiting use Time.stop()"""
        cls.__active = True
        for i in range(seconds):
            if cls.__active:
                time.sleep(1)
            else:
                break

    @classmethod
    def wait_for_ms(cls, ms):
        """Stops a program for 'ms' milliseconds.\n
            important!!! this function is unstoppable"""
        time.sleep(ms)

    @classmethod
    def stop(cls):
        cls.__active = False

    class Timer:
        def __init__(self):
            Time.timers.append(self)
            self.__thread = Thread(target=self.__start)
            self.time = 0
            self.stopped = False

        def start(self):
            self.__thread.start()

        def stop(self):
            self.stopped = True

        def __start(self):
            self.stopped = False
            t = round(time.time())
            while not self.stopped:
                d = round(time.time()) - t
                if d != self.time:
                    self.time = d