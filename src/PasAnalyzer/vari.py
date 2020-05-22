from PasAnalyzer.AST import AstNode


# ---------------------------------VariableNode-------------------------
class VariableNode(AstNode):
    def __init__(self, _id, _var_type):
        super().__init__()
        self.id = _id
        self.var_type = _var_type


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
        if value == 'true' or value == 'false':
            self.type = 'bool'
        else:
            self.type = ntype
        self.value = value

    def reverse(self):
        self.value = -self.value
