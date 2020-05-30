from PasAnalyzer.AST import AstNode, sym_table


# ---------------------------------ExpressionNode-------------------------
class ConstExprNode(AstNode):
    def __init__(self, lineno, _id, const_value):
        super().__init__()
        self.lineno = int(lineno)
        self.id = _id
        self.const_value = const_value
    
    def type_check(self):
        return True

class CaseExprNode(AstNode):
    def __init__(self, lineno, const_value, stmt):
        super().__init__()
        self.lineno = int(lineno)
        self.const_value = const_value
        self.stmt = stmt

    def type_check(self):
        return True

class BinaryExprNode(AstNode):
    def __init__(self, lineno, op, lexpr, rexpr):
        super().__init__()
        self.lineno = int(lineno)
        self.op = op
        self.lexpr = lexpr
        self.rexpr = rexpr

    def type_check(self):
        return True

class UnaryExprNode(AstNode):
    def __init__(self, lineno, op, factor):
        super().__init__()
        self.lineno = int(lineno)
        self.op = op
        self.factor = factor
        
    def type_check(self):
        return True