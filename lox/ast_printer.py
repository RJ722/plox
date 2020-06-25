from lox import Expr
from lox.visitor import Visitor
from lox.token import Token
from lox.tokentype import TokenType


class ASTPrinter(Visitor):
    def pprint_ast(self, expr):
        return self.visit(expr)

    def parenthesize(self, name, *args):
        out = ["(", name]
        for expr in args:
            out.append(" ")
            out.append(expr.accept(self))
        out.append(")")
        return "".join(out)

    def visit_BinaryExpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_GroupingExpr(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_LiteralExpr(self, expr):
        if expr.value == "nil":
            return "nil"
        return str(expr.value)

    def visit_UnaryExpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)


if __name__ == "__main__":
    expression = Expr.Binary(
        Expr.Unary(Token(TokenType.MINUS, "-", None, 1), Expr.Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Expr.Grouping(Expr.Literal(45.67)),
    )
    ppast = ASTPrinter().pprint_ast(expression)
    print(ppast)
