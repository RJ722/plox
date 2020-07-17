from lox.LoxCallable import LoxCallable

import time


class Clock(LoxCallable):
    @property
    def arity(self):
        return 0

    def __call__(self, interpreter, arguments):
        return time.time()

    def __str__(self):
        return "<native fn>"
