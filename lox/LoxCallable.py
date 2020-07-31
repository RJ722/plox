print('LoxCallable called!')

print('extra log which no one asked for')

print('I am thinking of adding another one. Oh, wait, I already did! ;)')

print('Last one, I promise!')


class LoxCallable:
    def __call__(self, interpreter, arguments):
        pass

    @property
    def arity(self):
        return
