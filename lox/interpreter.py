from lox.environment import Environment
from lox.exceptions import RuntimeException
from lox.LoxCallable import LoxCallable
from lox.LoxFunction import LoxFunction
from lox.native_functions import Clock
from lox.loxreturn import Return
from lox.tokentype import TokenType
from lox.visitor import Visitor


def _is_true(obj):
    """Only `nil` and `false` are false. Everything else _evaluates to true.
    """
    if obj == None:
        return False
    elif isinstance(obj, bool):
        return obj
    return True


def _check_num_operand(op, *numbers):
    for num in numbers:
        if not isinstance(num, float):
            raise RuntimeException(op, "Operand must be a number.")


def stringify(obj):
    if obj == None:
        return "nil"
    if isinstance(obj, bool):
        # Lox doesn't capitalize the starting 't' and 'f'.
        if obj:
            return "true"
        return "false"
    return str(obj)


class Interpreter(Visitor):
    # self.environment points towards the current environment, whereas
    # `global_env` always points to the outermost environment.
    # However, due to the implementation, it is shared amongst all instances.
    global_env = Environment()

    def __init__(self, lox):
        self.lox = lox
        self.global_env.define("clock", Clock())
        self.environment = self.global_env
        self.locals = {}

    def _execute(self, stmt):
        return self.visit(stmt)

    def _evaluate(self, expr):
        return self.visit(expr)

    def _lookup_variable(self, name, expr):
        distance = self.locals.get(expr, None)
        if distance != None:
            return self.environment.getat(distance, name)
        return self.global_env.get(name)

    def interpret(self, statements):
        try:
            for statement in statements:
                self._execute(statement)
        except RuntimeException as err:
            self.lox.runtime_error(err)

    def resolve(self, expr, depth):
        self.locals[expr] = depth

    def visit_LiteralExpr(self, expr):
        return expr.value

    def visit_GroupingExpr(self, expr):
        return self._evaluate(expr.expression)

    def visit_UnaryExpr(self, expr):
        right = self._evaluate(expr.right)

        if expr.operator.tokentype == TokenType.MINUS:
            _check_num_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.tokentype == TokenType.BANG:
            return not _is_true(right)
        return

    def visit_BinaryExpr(self, expr):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        if expr.operator.tokentype == TokenType.PLUS:
            # This handles both the cases - when (left, right) are float or str
            try:
                return left + right
            except TypeError:
                raise RuntimeException(
                    expr.operator,
                    "Operands must be two numbers or two strings.")
        elif expr.operator.tokentype == TokenType.MINUS:
            _check_num_operand(expr.operator, left, right)
            return left - right
        elif expr.operator.tokentype == TokenType.STAR:
            _check_num_operand(expr.operator, left, right)
            return left * right
        elif expr.operator.tokentype == TokenType.SLASH:
            _check_num_operand(expr.operator, left, right)
            if right == 0:
                raise RuntimeException(expr.operator, "Cannot divide by zero.")
            return left / right
        elif expr.operator.tokentype == TokenType.GREATER:
            _check_num_operand(expr.operator, left, right)
            return left > right
        elif expr.operator.tokentype == TokenType.GREATER_EQUAL:
            _check_num_operand(expr.operator, left, right)
            return left >= right
        elif expr.operator.tokentype == TokenType.LESS:
            _check_num_operand(expr.operator, left, right)
            return left < right
        elif expr.operator.tokentype == TokenType.LESS_EQUAL:
            _check_num_operand(expr.operator, left, right)
            return left <= right
        elif expr.operator.tokentype == TokenType.BANG_EQUAL:
            return left != right
        elif expr.operator.tokentype == TokenType.EQUAL_EQUAL:
            return left == right
        return

    def visit_VariableExpr(self, expr):
        return self._lookup_variable(expr.name, expr)

    def visit_AssignExpr(self, expr):
        value = self._evaluate(expr.value)
        distance = self.locals.get(expr, None)
        if distance != None:
            self.environment.assignat(distance, expr.name, value)
        else:
            self.global_env.assign(expr.name, value)
        return value

    def visit_LogicalExpr(self, expr):
        left = self._evaluate(expr.left)
        if expr.operator.tokentype == TokenType.OR:
            if _is_true(left):
                return left
        else:  # AND
            if not _is_true(left):
                return left
        return self._evaluate(expr.right)

    def visit_CallExpr(self, expr):
        callee = self._evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self._evaluate(argument))
        # callee - what would be the type of callee?
        if not isinstance(callee, LoxCallable):
            raise RuntimeException(expr.paren,
                                   "Can only call functions and classes.")

        # The original author, while writing this compiler in Java typecasted
        # the callee to LoxCallable, even after checking `isinstance(callee,
        # LoxCallable`. It isn't clear why. But, I'm apprehensive that this was
        # to satisfy some weird Inheritance rules of Java.

        # Since there is no explicit type casting mechanism in Python, (or there
        # is, and I'm not aware of it.) I will assume that the `isinstance`
        # check is enough and won't do the check.

        # The following line is commented out for documentation reasons.
        # function = LoxCallable(callee)

        if len(arguments) != callee.arity:
            raise RuntimeException(
                expr.paren,
                f"Expected {function.arity} arguments, but got {len(arguments)}.",
            )
        return callee.__call__(self, arguments)

    def visit_ExpressionStmt(self, stmt):
        self._evaluate(stmt.expression)

    def visit_PrintStmt(self, stmt):
        print(stringify(self._evaluate(stmt.expression)))

    def visit_VarStmt(self, stmt):
        value = None
        if stmt.initializer != None:
            value = self._evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def _execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self._execute(statement)
        finally:
            self.environment = previous

    def visit_BlockStmt(self, stmt):
        self._execute_block(stmt.statements, Environment(self.environment))

    def visit_IfStmt(self, stmt):
        if _is_true(self._evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch != None:
            self._execute(stmt.else_branch)

    def visit_WhileStmt(self, stmt):
        while _is_true(self._evaluate(stmt.condition)):
            self._execute(stmt.body)

    def visit_FunctionStmt(self, stmt):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)

    def visit_ReturnStmt(self, stmt):
        value = stmt.value
        if value != None:
            value = self._evaluate(stmt.value)
        raise Return(value)
