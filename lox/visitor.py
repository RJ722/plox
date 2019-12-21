class Visitor:
    def visit(self, expr_or_stmt):
        return expr_or_stmt.accept(self)

    def visit_AssignExpr(self, expr):
        pass

    def visit_BinaryExpr(self, expr):
        pass

    def visit_GroupingExpr(self, expr):
        pass

    def visit_LiteralExpr(self, expr):
        pass

    def visit_LogicalExpr(self, expr):
        pass

    def visit_UnaryExpr(self, expr):
        pass

    def visit_VariableExpr(self, expr):
        pass

    def visit_CallExpr(self, expr):
        pass

    def visit_BlockStmt(self, stmt):
        pass

    def visit_ExpressionStmt(self, stmt):
        pass

    def visit_PrintStmt(self, stmt):
        pass

    def visit_VarStmt(self, stmt):
        pass

    def visit_IfStmt(self, stmt):
        pass

    def visit_WhileStmt(self, stmt):
        pass

    def visit_FunctionStmt(self, stmt):
        pass

    def visit_ReturnStmt(self, stmt):
        pass
