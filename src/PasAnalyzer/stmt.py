from PasAnalyzer.AST import AstNode


# ---------------------------------StatementNode-------------------------
class StmtNode(AstNode):
    def __init__(self, line, stmt, _id=None):
        super().__init__()
        self.lineno = int(line)
        self.id = _id
        self.stmt_node = stmt


class AssignStmtNode(AstNode):
    def __init__(self, line, element_node, expression):
        super().__init__()
        self.lineno = int(line)
        self.expression = expression
        self.element_node = element_node


class IfStmtNode(AstNode):
    def __init__(self, line, expression, stmt, else_clause):
        super().__init__()
        self.lineno = int(line)
        self.expression = expression
        self.stmt = stmt
        self.else_clause = else_clause


class RepeatStmtNode(AstNode):
    def __init__(self, line, stmt_list, expression):
        super().__init__()
        self.lineno = int(line)
        self.stmt_list = stmt_list
        self.expression = expression


class WhileStmtNode(AstNode):
    def __init__(self, line, expression, stmt):
        super().__init__()
        self.lineno = int(line)
        self.expression = expression
        self.stmt = stmt


class ForStmtNode(AstNode):
    def __init__(self, line, name, expression1, direction, expression2, stmt):
        super().__init__()
        self.lineno = int(line)
        self.name = name
        self.expression1 = expression1
        self.direction = direction
        self.expression2 = expression2
        self.stmt = stmt


class CaseStmtNode(AstNode):
    def __init__(self, line, expression, case_expr_list):
        super().__init__()
        self.lineno = int(line)
        self.expression = expression
        self.case_expr_list = case_expr_list


class GotoStmtNode(AstNode):
    def __init__(self, line, num):
        super().__init__()
        self.lineno = int(line)
        self.num = num


class CallStmtNode(AstNode):
    def __init__(self, line, name, args_list):
        super().__init__()
        self.lineno = int(line)
        self.func_name = name
        self.args_list = args_list
