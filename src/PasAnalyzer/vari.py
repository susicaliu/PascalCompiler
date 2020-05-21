from PasAnalyzer.AST import AstNode
#---------------------------------VariableNode-------------------------
class VariableNode(AstNode):
    def __init__(self, _id):
        super().__init__()
        self.id = _id

class ArrayElementNode(AstNode):
    def __init__(self, _id, expression_array):
        super().__init__()
        self.id = _id
        self.expression_array = expression_array

class RecordElementNode(AstNode):
    def __init__(self, id1, id2):
        super().__init__()
        self.id = id1
        self.id2 = id2

class ConstValueNode(AstNode):
    def __init__(self, ntype, value):
        super().__init__()
        self.type = ntype
        self.value = value