from PasAnalyzer.AST import AstNode, sym_table
from PasError.myerrors import *
from PasError.mywarnings import *

# ---------------------------------StatementNode-------------------------
class StmtNode(AstNode):
    def __init__(self, line, stmt, _id=None):
        super().__init__()
        self.lineno = int(line)
        self.id = _id
        self.stmt_node = stmt

    def type_check(self):
        return True

class AssignStmtNode(AstNode):
    def __init__(self, line, element_node, expression):
        super().__init__()
        self.lineno = int(line)
        self.expression = expression
        self.element_node = element_node

    def type_check(self):
        rhs_exi = sym_table.has_vari(self.element_node)
        if rhs_exi is None:
            SyntxError(self.element_node, self.lineno, self.colno).log()
        else:
            rhs_type = sym_table.get_vari_type(self.element_node) 
            lhs = self.expression.type_check()
            if check_rhs(rhs_type) and check_lhs(lhs):
                ans = self.cmp(rhs_type,lhs)
                if ans == 0:
                    return rhs_type
                else:
                    TypeWarning(self.element_node, self.lineno, self.colno).log()
                    if ans > 0:
                        return rhs_type
                    else:
                        return lhs
            else:
                TypError(self.element_node, self.lineno, self.colno).log()

class IfStmtNode(AstNode):
    def __init__(self, line, expression, stmt, else_clause):
        super().__init__()
        self.lineno = int(line)
        self.expression = expression
        self.stmt = stmt
        self.else_clause = else_clause

    def type_check(self):
        return True

class RepeatStmtNode(AstNode):
    def __init__(self, line, stmt_list, expression):
        super().__init__()
        self.lineno = int(line)
        self.stmt_list = stmt_list
        self.expression = expression

    def type_check(self):
        return True

class WhileStmtNode(AstNode):
    def __init__(self, line, expression, stmt):
        super().__init__()
        self.lineno = int(line)
        self.expression = expression
        self.stmt = stmt

    def type_check(self):
        return True

class ForStmtNode(AstNode):
    def __init__(self, line, name, expression1, direction, expression2, stmt):
        super().__init__()
        self.lineno = int(line)
        self.name = name
        self.expression1 = expression1
        self.direction = direction
        self.expression2 = expression2
        self.stmt = stmt

    def type_check(self):
        return True

class CaseStmtNode(AstNode):
    def __init__(self, line, expression, case_expr_list):
        super().__init__()
        self.lineno = int(line)
        self.expression = expression
        self.case_expr_list = case_expr_list

    def type_check(self):
        return True

class GotoStmtNode(AstNode):
    def __init__(self, line, num):
        super().__init__()
        self.lineno = int(line)
        self.num = num

    def type_check(self):
        return True

class CallStmtNode(AstNode):
    def __init__(self, line, name, args_list):
        super().__init__()
        self.lineno = int(line)
        self.func_name = name
        self.args_list = args_list

    def type_check(self):
        return True