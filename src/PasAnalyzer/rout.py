from PasAnalyzer.AST import AstNode
#---------------------------------RoutineNode-------------------------
class RoutineNode(AstNode):
    def __init__(self, routine_head, routine_body):
        super().__init__()
        self.routine_head = routine_head
        self.routine_body = routine_body

class SubRoutineNode(AstNode):
    def __init__(self, routine_head, routine_body):
        super().__init__()
        self.routine_head = routine_head
        self.routine_body = routine_body

class RoutineHeadNode(AstNode):
    def __init__(self, label_part, const_part, type_part, var_part, routine_part):
        super().__init__()
        self.label_part = label_part
        self.const_part = const_part
        self.type_part = type_part
        self.var_part = var_part
        self.routine_part = routine_part

class FunctionDeclNode(AstNode):
    def __init__(self, function_head, sub_routine):
        super().__init__()
        self.function_head = function_head
        self.sub_routine = sub_routine

class FunctionHeadNode(AstNode):
    def __init__(self, id, parameters, simple_type_decl):
        super().__init__()
        self.id = id
        self.parameters = parameters
        self.simple_type_decl = simple_type_decl


class ProcedureDeclNode(AstNode):
    def __init__(self, procedure_head, sub_routine):
        super().__init__()
        self.procedure_head = procedure_head
        self.sub_routine = sub_routine


class ProcedureHeadNode(AstNode):
    def __init__(self, _id, parameters):
        super().__init__()
        self.id = _id
        self.parameters = parameters