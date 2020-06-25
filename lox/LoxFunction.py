from lox.environment import Environment
from lox.LoxCallable import LoxCallable
from lox.loxreturn import Return


class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def __call__(self, interpreter, arguments):
        self.environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            self.environment.define(self.declaration.params[i].lexeme,
                                    arguments[i])
        try:
            interpreter._execute_block(self.declaration.body, self.environment)
        except Return as ret:
            return ret.value

    @property
    def arity(self):
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
