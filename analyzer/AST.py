
class AstNode(object):
    def __init__(self):
        super().__init__()


class ProgramNode(AstNode):
    def __init__(self, program_head, routine):
        super().__init__()
        self.routine = routine
        self.program_head = program_head


class ProgramHeadNode(AstNode):
    def __init__(self,id):
        super().__init__()
        self.id=id


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

class VariableNode(AstNode):
    def __init__(self,id):
        super().__init__()
        self.id=id
    def set_id(self,id):
        self.id=id

class ArrayElementNode(AstNode):
    def __init__(self,id,expression_array):
        super().__init__()
        self.id=id
        self.expression_array=expression_array
    def set_id(self,id):
        self.id=id

class RecordElementNode(AstNode):
    def __init__(self,id,id2):
        super().__init__()
        self.id=id
        self.id2=id2
    def set_id(self,id):
        self.id=id

class ConstExprNode(AstNode):
    def __init__(self,variable_node,const_value):
        super().__init__()
        self.variable_node=variable_node
        self.const_value=const_value



class TypeDefinitionNode(AstNode):
    def __init__(self, id, type_decl):
        super().__init__()
        self.id = id
        self.type_decl = type_decl


class ConstValueNode(AstNode):
    def __init__(self,name, type,value):
        super().__init__()
        self.type = type
        self.value=value



class VarDeclNode(AstNode):
    def __init__(self, name_list, type_decl):
        super().__init__()
        self.name_list = name_list
        self.type_decl = type_decl

class FunctionHeadNode(AstNode):
    def __init__(self,id, parameters, simple_type_decl):
        super().__init__()
        self.id=id
        self.parameters = parameters
        self.simple_type_decl = simple_type_decl

class ProcedureDeclNode(AstNode):
    def __init__(self, procedure_head, sub_routine):
        super().__init__()
        self.procedure_head = procedure_head
        self.sub_routine = sub_routine


class ProcedureHeadNode(AstNode):
    def __init__(self,id,parameters):
        super().__init__()
        self.id=id
        self.parameters=parameters
# -----------------------------------StmtNode-------------------------------------

class AssignStmtNode(AstNode):
    def __init__(self,element_node,expression):
        super().__init__()
        self.expression=expression
        self.element_node=element_node
    def set_id(self,id):
        self.element_node.set_id(id)

class IfStmtNode(AstNode):
    def __init__(self, expression, stmt, else_clause):
        super().__init__()
        self.expression = expression
        self.stmt = stmt
        self.else_clause = else_clause

class RepeatStmtNode(AstNode):
    def __init__(self, stmt_list, expression):
        super().__init__()
        self.stmt_list = stmt_list
        self.expression = expression


class WhileStmtNode(AstNode):
    def __init__(self, expression,stmt):
        super().__init__()
        self.expression = expression
        self.stmt = stmt


class ForStmtNode(AstNode):
    def __init__(self,id, expression1, direction, expression2, stmt):
        super().__init__()
        self.id=id
        self.expression1 = expression1
        self.direction = direction
        self.expression2 = expression2
        self.stmt = stmt

class CaseStmtNode(AstNode):
    def __init__(self, expression, case_expr_list):
        super().__init__()
        self.expression = expression
        self.case_expr_list = case_expr_list

#---------------------------------expressionNode-------------------------

class CallExprNode(AstNode):
    def __init__(self, id, args_list):
        super().__init__()
        self.id = id
        self.args_list = args_list

class CaseExprNode(AstNode):
    def __init__(self, const_value, stmt):
        super().__init__()
        self.const_value = const_value
        self.stmt = stmt

class BinaryExprNode(AstNode):
    def __init__(self, op, lexpr,rexpr):
        super().__init__()
        self.op = op
        self.lexpr = lexpr
        self.rexpr=rexpr

class UnaryExprNode(AstNode):
    def __init__(self, op, factor):
        super().__init__()
        self.op = op
        self.factor = factor

# --------------------------TypeDeclNode-------------------------------------

class SimpleTypeDeclNode(TypeNode):
    def __init__(self,type_name):
        super().__init__()
        self.type_name=type_name

class VariableTypeDeclNode(TypeNode):
    def __init__(self,id):
        super().__init__()
        self.id=id

class ArrayTypeDeclNode(TypeNode):
    def __init__(self, simple_type_decl, type_decl):
        super().__init__()
        self.simple_type_decl = simple_type_decl
        self.type_decl = type_decl

class EnumTypeDeclNode(TypeNode):
    def __init__(self, name_list):
        super().__init__()
        self.name_list = name_list

class RecordTypeDeclNode(TypeNode):
    def __init__(self, field_decl_list):
        super().__init__()
        self.field_decl_list = field_decl_list


class RangeTypeNode(TypeNode):
    def __init__(self, num1,const_value1,num2,const_value2):
        self.num1 = num1
        self.const_value1 = const_value1
        self.num2 = num2 
        self.const_value2 = const_value2

# --------------------------ListNode-------------------------------------


class ListNode(AstNode):
    def __init__(self, node=None):
        super().__init__()
        self.NodeList = []
        if node is not None:
            self.NodeList.append(node)

    def append(self, node):
        self.NodeList.append(node)


class ConstExprListNode(ListNode):
    def __init__(self):
        super().__init__()


class TypeDeclListNode(ListNode):
    def __init__(self):
        super().__init__()


class FieldDeclListNode(ListNode):
    def __init__(self):
        super().__init__()


class VarDeclListNode(ListNode):
    def __init__(self):
        super().__init__()


class ParaDeclListNode(ListNode):
    def __init__(self):
        super().__init__()


class ParaTypeListNode(ListNode):
    def __init__(self):
        super().__init__()

class NameListNode(ListNode):
    def __init__(self):
        super().__init__()


class StmtListNode(ListNode):
    def __init__(self):
        super().__init__()


class CaseExprListNode(ListNode):
    def __init__(self):
        super().__init__()


class ArgsListNode(ListNode):
    def __init__(self):
        super().__init__()

class FunctionDeclListNode(ListNode):
    def __init__(self):
        super().__init__()

class ProcedureDeclListNode(ListNode):
    def __init__(self):
        super().__init__()


class CaseExprListNode(ListNode):
    def __init__(self):
        super().__init__()
