from PasAnalyzer.AST import AstNode
#---------------------------------ExpressionNode-------------------------
class ConstExprNode(AstNode):
    def __init__(self, _id, const_value):
        super().__init__()
        self.id = _id
        self.const_value = const_value
        
class CaseExprNode(AstNode):
    def __init__(self, const_value, stmt):
        super().__init__()
        self.const_value = const_value
        self.stmt = stmt


class BinaryExprNode(AstNode):
    def __init__(self, op, lexpr, rexpr):
        super().__init__()
        self.op = op
        self.lexpr = lexpr
        self.rexpr = rexpr


class UnaryExprNode(AstNode):
    def __init__(self, op, factor):
        super().__init__()
        self.op = op
        self.factor = factor