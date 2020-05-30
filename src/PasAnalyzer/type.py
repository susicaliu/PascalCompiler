from PasAnalyzer.AST import AstNode, sym_table


# --------------------------TypeNode-------------------------------------
class TypeDefinitionNode(AstNode):
    def __init__(self, lineno, _id, type_decl):
        super().__init__()
        self.lineno = int(lineno)
        self.id = _id
        self.type_decl = type_decl

    def type_check(self):
        return True

class SimpleTypeDeclNode(AstNode):
    def __init__(self, lineno, _id):
        super().__init__()
        self.id = _id
        self.lineno = int(lineno)

    def type_check(self):
        return True

class VariableTypeDeclNode(AstNode):
    def __init__(self, lineno, _id):
        super().__init__()
        self.id = _id
        self.lineno = int(lineno)

    def type_check(self):
        return True

class ArrayTypeDeclNode(AstNode):
    def __init__(self, lineno, simple_type_decl, type_decl):
        super().__init__()
        self.lineno = int(lineno)
        self.simple_type_decl = simple_type_decl
        self.type_decl = type_decl

    def type_check(self):
        return True

class EnumTypeDeclNode(AstNode):
    def __init__(self, lineno, name_list):
        super().__init__()
        self.lineno = int(lineno)
        self.name_list = name_list

    def type_check(self):
        return True

class RecordTypeDeclNode(AstNode):
    def __init__(self, lineno, field_decl_list):
        super().__init__()
        self.lineno = int(lineno)
        self.field_decl_list = field_decl_list

    def type_check(self):
        return True

class RangeTypeDeclNode(AstNode):
    def __init__(self, lineno, const_value1, const_value2):
        super().__init__()
        self.lineno = int(lineno)
        self.const_value1 = const_value1
        self.const_value2 = const_value2

    def type_check(self):
        return True

class VarDeclNode(AstNode):
    def __init__(self, lineno, name_list, type_decl):
        super().__init__()
        self.lineno = int(lineno)
        self.name_list = name_list
        self.type_decl = type_decl

    def type_check(self):
        return True

class FieldDeclNode(AstNode):
    def __init__(self, lineno, name_list, type_decl):
        super().__init__()
        self.lineno = int(lineno)
        self.name_list = name_list
        self.type_decl = type_decl

    def type_check(self):
        return True