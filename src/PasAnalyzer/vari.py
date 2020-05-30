from PasAnalyzer.AST import AstNode, sym_table
from PasError.myerrors import *

# ---------------------------------VariableNode-------------------------
class VariableNode(AstNode):
    def __init__(self, lineno, _id, _var_type):
        super().__init__()
        self.lineno = int(lineno)
        self.id = _id
        self.var_type = _var_type

    def type_check(self):
        vari = sym_table.has_vari(self.id)
        vari_type = sym_table.get_vari_type(self.id)
        if vari:
            return vari_type
        else:
            DefineError(self.id, self.lineno, 1).log()

class ArrayElementNode(AstNode):
    def __init__(self, lineno, _id, expression_array):
        super().__init__()
        self.lineno = int(lineno)
        self.id = _id
        self.expression_array = expression_array

    def type_check(self):
        vari = sym_table.has_vari(self.id)
        vari_type = sym_table.get_vari_type(self.id)
        if vari:
            return True
        else:
            DefineError(self.id, self.lineno, 1).log()

class RecordElementNode(AstNode):
    def __init__(self, lineno, id1, id2):
        super().__init__()
        self.lineno = int(lineno)
        self.id = id1
        self.id2 = id2

    def type_check(self):
        vari = sym_table.has_reco(self.id,self.id2)
        vari_type = sym_table.get_vari_type(self.id)
        if vari:
            return True
        else:
            DefineError(self.id, self.lineno, 1).log()

class ConstValueNode(AstNode):
    def __init__(self, lineno, ntype, value):
        super().__init__()
        self.lineno = int(lineno)
        if value == 'true' or value == 'false':
            self.type = 'bool'
        else:
            self.type = ntype
        self.value = value

    def reverse(self):
        self.value = -self.value

    def type_check(self):
        return True