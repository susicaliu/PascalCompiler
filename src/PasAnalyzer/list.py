from PasAnalyzer.AST import ListNode, AstNode, sym_table


# --------------------------ListNode-------------------------------------
class ConstExprListNode(ListNode):
    def __init__(self, lineno, node):
        super().__init__(lineno, node)

class TypeDeclListNode(ListNode):
    def __init__(self, lineno, node):
        super().__init__(lineno, node)


class FieldDeclListNode(ListNode):
    def __init__(self, lineno, node):
        super().__init__(lineno, node)


class VarDeclListNode(ListNode):
    def __init__(self, lineno, node):
        super().__init__(lineno, node)

class ParaDeclListNode(ListNode):
    def __init__(self, lineno, node):
        super().__init__(lineno, node)


class NameListNode(ListNode):
    def __init__(self, lineno, node):
        super().__init__(lineno, node)

    def set_type(self, _type_name):
        for var in self.NodeList:
            if var is not None:
                var.var_type = _type_name


class StmtListNode(ListNode):
    def __init__(self, lineno, node):
        super().__init__(lineno, node)


class CaseExprListNode(ListNode):
    def __init__(self, lineno, node):
        super().__init__(lineno, node)

class ExprListNode(ListNode):
    def __init__(self, lineno, node):
        super().__init__(lineno, node)

class ArgsListNode(ListNode):
    def __init__(self, lineno, node):
        super().__init__(lineno, node)

class RoutineDeclListNode(ListNode):
    def __init__(self, lineno, node, _id):
        super().__init__(lineno, node)
        self.id = _id
