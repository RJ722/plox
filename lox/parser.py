from lox import Expr
from lox.exceptions import ParseException
from lox import Stmt
from lox.tokentype import TokenType


class Parser:
    def __init__(self, tokens, lox):
        self.tokens = tokens
        self.current = 0
        self.lox = lox

    def _check(self, matchtype):
        if self._at_end():
            return False
        return self._peek().tokentype == matchtype

    @property
    def _previous(self):
        return self.tokens[self.current - 1]

    def _peek(self):
        return self.tokens[self.current]

    def _advance(self):
        if not self._at_end():
            self.current = self.current + 1
        return self._previous

    def _at_end(self):
        return self._peek().tokentype == TokenType.EOF

    def _match(self, matchtypes):
        for matchtype in matchtypes:
            if self._check(matchtype):
                self._advance()
                return True
        return False

    def _error(self, token, message):
        self.lox.error(token, message)
        return ParseException(message)

    def _consume(self, tokentype, message):
        if self._check(tokentype):
            return self._advance()
        raise self._error(self._peek(), message)

    def _finish_call(self, callee):
        arguments = []
        if not self._check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self._match([TokenType.COMMA]):
                arguments.append(self.expression())
        paren = self._consume(TokenType.RIGHT_PAREN,
                              "Expected ')' after arguments.")
        if len(arguments) > 255:
            self._error(self._peek(), "Cannot have more than 255 arguments.")
        return Expr.Call(callee, paren, arguments)

    def declaration(self):
        try:
            if self._match([TokenType.VAR]):
                return self.var_declaration()
            elif self._match([TokenType.FUN]):
                return self.function_declaration("function")
            return self.statement()
        except ParseException:
            self._synchronize()

    def function_declaration(self, kind):
        """We reuse this method for both function and method declaration.
           `kind` is used to distinguish between the two.
        """
        name = self._consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self._consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self._check(TokenType.RIGHT_PAREN):
            parameters.append(
                self._consume(TokenType.IDENTIFIER, "Expect parameter name."))
            while self._match([TokenType.COMMA]):
                parameters.append(
                    self._consume(TokenType.IDENTIFIER,
                                  "Expect parameter name."))
        if len(parameters) > 255:
            self._error(self._peek(), "Cannot have more than 255 parameters.")
        self._consume(TokenType.RIGHT_PAREN, "Expect ')'after parameters.")
        self._consume(TokenType.LEFT_BRACE,
                      "Expect '{' before" + kind + "body.")
        body = self.block()
        return Stmt.Function(name, parameters, body)

    def var_declaration(self):
        name = self._consume(TokenType.IDENTIFIER, "Expect variable name.")
        value = self.expression() if self._match([TokenType.EQUAL]) else None
        self._consume(TokenType.SEMICOLON,
                      "Expect ';' after variable declaration.")
        return Stmt.Var(name, value)

    def statement(self):
        if self._match([TokenType.FOR]):
            return self.for_statement()
        if self._match([TokenType.IF]):
            return self.if_statement()
        if self._match([TokenType.PRINT]):
            return self.print_statement()
        if self._match([TokenType.RETURN]):
            return self.return_statement()
        if self._match([TokenType.WHILE]):
            return self.while_statement()
        if self._match([TokenType.LEFT_BRACE]):
            return Stmt.Block(self.block())
        return self.expression_statement()

    def block(self):
        statements = []
        while (not self._check(
                TokenType.RIGHT_BRACE)) and (not self._at_end()):
            statements.append(self.declaration())
        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def return_statement(self):
        keyword = self._previous
        value = None
        if not self._check(TokenType.SEMICOLON):
            value = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Stmt.Return(keyword, value)

    def for_statement(self):
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        if self._match([TokenType.SEMICOLON]):
            initializer = None
        elif self._match([TokenType.VAR]):
            initializer = self.var_declaration()
        else:
            initializer = self.expression()

        condition = Expr.Literal(True)
        if not self._check(TokenType.SEMICOLON):
            condition = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        incrementor = None
        if not self._check(TokenType.RIGHT_PAREN):
            incrementor = self.expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ') after for clauses.")
        body = self.statement()

        # Lox Code - `for (var a = 0; a < 3; a = a + 1) print a;`
        # is ~transalated~ desugared into:
        # {                     // This additional Block limits the scope
        #     var a = 0;
        #     while (a < 3){
        #         print a;
        #         a = a + 1;
        #     }
        # }

        if incrementor != None:
            body = Stmt.Block([body, incrementor])
        body = Stmt.While(condition, body)
        if initializer != None:
            body = Stmt.Block([initializer, body])

        return body

    def while_statement(self):
        self._consume(TokenType.LEFT_PAREN, "Expect ')' after while.")
        condition = self.expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return Stmt.While(condition, body)

    def if_statement(self):
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self._match([TokenType.ELSE]):
            else_branch = self.statement()

        return Stmt.If(condition, then_branch, else_branch)

    def print_statement(self):
        value = self.expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after expression.")
        return Stmt.Print(value)

    def expression_statement(self):
        expression = self.expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after expression.")
        return Stmt.Expression(expression)

    def expression(self):
        return self.assignment()

    def assignment(self):
        # Parse the left hand sign as an higher precedent expression
        expr = self.logical_or()
        if self._match([TokenType.EQUAL]):
            equals = self._previous
            value = self.assignment()
            if isinstance(expr, Expr.Variable):
                return Expr.Assign(expr.name, value)
            # If LHS isn't writable, raise ParseError
            self._error(equals, "Invalid assignment target.")
        return expr

    def logical_or(self):
        expr = self.logical_and()
        while self._match([TokenType.OR]):
            operator = self._previous
            right = self.logical_and()
            expr = Expr.Logical(expr, operator, right)
        return expr

    def logical_and(self):
        expr = self.equality()
        while self._match([TokenType.AND]):
            operator = self._previous
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)
        return expr

    def equality(self):
        expr = self.comparison()
        while self._match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self._previous
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.addition()
        while self._match([
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
        ]):
            operator = self._previous
            right = self.addition()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def addition(self):
        expr = self.multiplication()
        while self._match([TokenType.PLUS, TokenType.MINUS]):
            operator = self._previous
            right = self.multiplication()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def multiplication(self):
        expr = self.unary()
        while self._match([TokenType.STAR, TokenType.SLASH]):
            operator = self._previous
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def unary(self):
        if self._match([TokenType.MINUS, TokenType.BANG]):
            operator = self._previous
            right = self.unary()
            expr = Expr.Unary(operator, right)
            return expr
        return self.call()

    def call(self):
        expr = self.primary()
        while True:
            if self._match([TokenType.LEFT_PAREN]):
                expr = self._finish_call(expr)
            else:
                break
        return expr

    def primary(self):
        if self._match([TokenType.FALSE]):
            return Expr.Literal(False)
        elif self._match([TokenType.TRUE]):
            return Expr.Literal(True)
        elif self._match([TokenType.NIL]):
            return Expr.Literal(None)
        elif self._match([TokenType.NUMBER, TokenType.STRING]):
            return Expr.Literal(self._previous.literal)
        elif self._match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self._consume(TokenType.RIGHT_PAREN,
                          "Expect ')' after expression.")
            return Expr.Grouping(expr)
        elif self._match([TokenType.IDENTIFIER]):
            return Expr.Variable(self._previous)
        raise self._error(self._peek(), "Expect expression.")

    def _synchronize(self):
        """Skip tokens until a new statement is found in case of an error.
        """
        self._advance()
        while not self._at_end():
            if self._previous == TokenType.SEMICOLON:
                return
            if self._peek().tokentype in (
                    TokenType.CLASS,
                    TokenType.FUN,
                    TokenType.VAR,
                    TokenType.FOR,
                    TokenType.IF,
                    TokenType.WHILE,
                    TokenType.PRINT,
                    TokenType.RETURN,
            ):
                return
            self._advance()

    def parse(self):
        statements = []
        while not self._at_end():
            statements.append(self.declaration())
        return statements
