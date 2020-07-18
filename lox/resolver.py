from enum import Enum

from lox.visitor import Visitor

FunctionType = Enum("FunctionType", ["NONE", "FUNCTION"])


class Resolver(Visitor):
    def __init__(self, lox, interpreter):
        self.interpreter = interpreter
        self.lox = lox
        self.scopes = []
        self.current_function = FunctionType.NONE

    @property
    def scope_is_empty(self):
        return len(self.scopes) == 0

    def _resolve(self, expr_or_stmt):
        return self.visit(expr_or_stmt)

    def resolve(self, stmts):
        if isinstance(stmts, list):
            for statement in stmts:
                self._resolve(statement)
        else:
            self._resolve(stmts)

    def resolve_local(self, expr, name):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i].keys():
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def resolve_function(self, stmt, function_type):
        enclosing_function = self.current_function
        self.current_function = function_type
        self._begin_scope()
        for param in stmt.params:
            self._declare(param)
            self._define(param)
        self.resolve(stmt.body)
        self._end_scope()
        self.current_function = enclosing_function

    def _begin_scope(self):
        self.scopes.append({})

    def _end_scope(self):
        self.scopes.pop()

    def _declare(self, name):
        if self.scope_is_empty:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope.keys():
            self.lox.error(
                name, "Variable with this name already declared in this scope."
            )
            # We don't need to return/stop here, because `self.lox.had_error`
            # gets set and no code would be interpreted.
        scope[name.lexeme] = False

    def _define(self, name):
        if self.scope_is_empty:
            return
        self.scopes[-1][name.lexeme] = True

    def visit_BlockStmt(self, stmt):
        self._begin_scope()
        self.resolve(stmt.statements)
        self._end_scope()

    def visit_VarStmt(self, stmt):
        self._declare(stmt.name)
        if stmt.initializer != None:
            self.resolve(stmt.initializer)
        self._define(stmt.name)

    def visit_FunctionStmt(self, stmt):
        self._declare(stmt.name)
        self._define(stmt.name)
        self.resolve_function(stmt, FunctionType)

    def visit_ExpressionStmt(self, stmt):
        self.resolve(stmt.expression)

    def visit_IfStmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch != None:
            self.resolve(stmt.else_branch)

    def visit_PrintStmt(self, stmt):
        self.resolve(stmt.expression)

    def visit_ReturnStmt(self, stmt):
        if self.current_function == FunctionType.NONE:
            self.lox.error(stmt.keyword, "Cannot return from top-level code.")
        if stmt.value != None:
            self.resolve(stmt.value)

    def visit_WhileStmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    def visit_VariableExpr(self, expr):
        if (not self.scope_is_empty) and self.scopes[-1].get(
            expr.name.lexeme, None
        ) == False:
            self.lox.error(
                expr.name, "Cannot read local variable in it's own initializer."
            )
        self.resolve_local(expr, expr.name)

    def visit_AssignExpr(self, expr):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_BinaryExpr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_CallExpr(self, expr):
        self.resolve(expr.callee)
        for arg in expr.arguments:
            self.resolve(arg)

    def visit_GroupingExpr(self, expr):
        self.resolve(expr.expression)

    def visit_LogicalExpr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_UnaryExpr(self, expr):
        self.resolve(expr.right)
