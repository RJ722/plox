from lox.exceptions import RuntimeException


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def ancestor(self, distance):
        for i in range(distance):
            self = self.enclosing
        return self

    def define(self, name, value):
        """:param name: str
           :param value: Expr.Literal
        """
        self.values[name] = value

    def assign(self, name, value):
        """:param name: Token
           :param value: Expr.Literal
        """
        if name.lexeme in self.values.keys():
            self.define(name.lexeme, value)
            return
        if self.enclosing != None:
            self.enclosing.assign(name, value)
            return
        raise RuntimeException(name, f"Undefined variable {name.lexeme}.")

    def get(self, name):
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        if self.enclosing != None:
            return self.enclosing.get(name)
        raise RuntimeException(name, f"Undefined name {name.lexeme}.")

    def getat(self, distance, name):
        return self.ancestor(distance).values[name.lexeme]

    def assignat(self, distance, name, value):
        self.ancestor(distance).values[name] = value
