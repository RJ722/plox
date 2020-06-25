from lox.token import Token
from lox.tokentype import TokenType

KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


class Scanner:
    def __init__(self, source, lox):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []
        self.lox = lox

    @property
    def at_end(self):
        return self.current >= len(self.source)

    def EOF(self):
        return Token(TokenType.EOF, "", None, self.line)

    def previous_token(self):
        if len(self.tokens) == 0:
            return self.EOF()
        return self.tokens[-1]

    def advance(self):
        self.current = self.current + 1
        return self.source[self.current - 1]

    def add_token(self, tokentype, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(tokentype, text, literal, self.line))

    def _peek(self):
        """
        Look up the current char in c. However, return EOF `\0` if at end.
        """
        if self.at_end:
            return "\0"
        return self.source[self.current]

    def _peek_next(self):
        if self.current + 1 > len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _is_next(self, expected):
        if self.at_end:
            return False
        if self.source[self.current] != expected:
            return False
        self.current = self.current + 1
        return True

    def _handle_number(self):
        while self._peek().isdigit():
            self.advance()

        # Check for fractional part
        if self._peek() == "." and self._peek_next().isdigit():
            self.advance()  # Consume the `.`
            while self._peek().isdigit():
                self.advance()

        literal = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, literal)

    def _handle_slash(self):
        if self._is_next(
                "/"):  # It is a comment. Ignore until end of line/file.
            while self._peek() != "\n" and not self.at_end:
                self.advance()
        else:
            self.add_token(TokenType.SLASH)

    def _handle_identifier(self):
        while self._peek().isalnum():
            self.advance()

        text = self.source[self.start:self.current]
        tokentype = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add_token(tokentype)

    def _handle_string(self):
        while self._peek() != '"' and not self.at_end:
            # Allow multi-line strings
            if self._peek() == "\n":
                self.line = self.line + 1
            self.advance()
        if self.at_end:
            self.lox.error(self.previous_token(), "Unterminated string.")
            return

        self.advance()  # Consume the ending `"`

        # Also save the literal value of the string
        literal = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, literal)

    def scan_token(self):
        c = self.advance()
        if c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "!":
            self.add_token(
                TokenType.BANG_EQUAL if self._is_next("=") else TokenType.BANG)
        elif c == "=":
            self.add_token(TokenType.EQUAL_EQUAL if self.
                           _is_next("=") else TokenType.EQUAL)
        elif c == "<":
            self.add_token(
                TokenType.LESS_EQUAL if self._is_next("=") else TokenType.LESS)
        elif c == ">":
            self.add_token(TokenType.GREATER_EQUAL if self.
                           _is_next("=") else TokenType.GREATER)
        elif c == "/":
            self._handle_slash()
        elif c in (" ", "\r", "\t"):  # Empty spaces
            pass
        elif c == "\n":
            self.line = self.line + 1
        elif c == '"':
            self._handle_string()
        else:
            if c.isdigit():
                self._handle_number()
            elif c.isalpha():
                self._handle_identifier()
            else:
                self.lox.error(self.previous_token(), "Unexpected character.")

    def scan_tokens(self):
        while not self.at_end:
            self.start = self.current
            self.scan_token()

        # Add EOF when done - We don't use `self.add_token` here because `EOF`
        # has no association with any `text`.
        self.tokens.append(self.EOF())
        return self.tokens
