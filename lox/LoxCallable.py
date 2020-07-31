print('LoxCallable called!')

print('extra log which no one asked for')

class LoxCallable:
    def __call__(self, interpreter, arguments):
        pass

    @property
    def arity(self):
        return
