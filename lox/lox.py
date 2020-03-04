import sys

from lox.interpreter import Interpreter
from lox.parser import Parser
from lox.resolver import Resolver
from lox.scanner import Scanner
from lox.tokentype import TokenType

class Lox:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False
        self.interpreter = Interpreter(self)
        self.resolver = Resolver(self, self.interpreter)

    def _report(self, line, where, message):
        # Should we pipe to `sys.stderr`?
        print(f'[Line {line}] Error{where}: {message}')

    def error(self, token, message):
        self.had_error = True
        if token.tokentype == TokenType.EOF:
            self._report(token.line, " at end", message)
        else:
            self._report(token.line, f" at '{token.lexeme}'", message)
    
    def runtime_error(self, err):
        print(f'[Line {err.token.line}] {err}')
        self.had_runtime_error = True

    def run_file(self, filename):
        with open(filename, 'r') as f:
            self.run(f.read())

        EXIT_CODE = 0
        if self.had_error:
            EXIT_CODE = 64
        elif self.had_runtime_error:
            EXIT_CODE = 70
        sys.exit(EXIT_CODE)

    def run_prompt(self):
        while True:
            reader = input('> ')
            self.run(reader)
            self.had_error = False

    def run(self, source):
        scanner = Scanner(source, self)
        tokens = scanner.scan_tokens()
        statements = Parser(tokens, self).parse()
        if self.had_error:
            return
        if self.had_error:
            return
        self.interpreter.interpret(statements)

def main():
    l = Lox()
    if len(sys.argv) > 2:
        print("Usage: lox {script}")
        sys.exit(64)
    elif len(sys.argv) == 2:
        l.run_file(sys.argv[1])
    else:
        l.run_prompt()


if __name__ == '__main__':
    main()
