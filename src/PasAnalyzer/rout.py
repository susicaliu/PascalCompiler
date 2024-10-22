from PasAnalyzer.AST import AstNode, sym_table
from PasError.myerrors import *

# ---------------------------------RoutineNode-------------------------
class RoutineNode(AstNode):
    def __init__(self, lineno, routine_head, routine_body):
        super().__init__()
        self.lineno = int(lineno)
        self.routine_head = routine_head
        self.routine_body = routine_body

    def type_check(self):
        return True

class SubRoutineNode(AstNode):
    def __init__(self, lineno, routine_head, routine_body):
        super().__init__()
        self.lineno = int(lineno)
        self.routine_head = routine_head
        self.routine_body = routine_body

    def type_check(self):
        return True

class RoutineHeadNode(AstNode):
    def __init__(self, lineno, label_part, const_part, type_part, var_part, routine_part):
        super().__init__()
        self.lineno = int(lineno)
        self.label_part = label_part
        self.const_part = const_part
        self.type_part = type_part
        self.var_part = var_part
        self.routine_part = routine_part

    def type_check(self):
        return True

class FunctionDeclNode(AstNode):
    def __init__(self, lineno, function_head, sub_routine):
        super().__init__()
        self.lineno = int(lineno)
        self.function_head = function_head
        self.sub_routine = sub_routine

    def type_check(self):
        func = sym_table.has_func(self.id)
        func_type = sym_table.get_func_type(self.id)
        if func:
            return func_type
        else:
            DefineError(self.id, self.lineno, self.colno).log()

class FunctionHeadNode(AstNode):
    def __init__(self, lineno, id, parameters, simple_type_decl):
        super().__init__()
        self.lineno = int(lineno)
        self.id = id
        self.parameters = parameters
        self.simple_type_decl = simple_type_decl
   
    def type_check(self):
        return True

class ProcedureDeclNode(AstNode):
    def __init__(self, lineno, procedure_head, sub_routine):
        super().__init__()
        self.lineno = int(lineno)
        self.procedure_head = procedure_head
        self.sub_routine = sub_routine

    def type_check(self):
        func = sym_table.has_func(self.id)
        func_type = sym_table.get_func_type(self.id)
        if func:
            return func_type
        else:
            DefineError(self.id, self.lineno, self.colno).log()

class ProcedureHeadNode(AstNode):
    def __init__(self, lineno, _id, parameters):
        super().__init__()
        self.lineno = int(lineno)
        self.id = _id
        self.parameters = parameters

    def type_check(self):
        return True