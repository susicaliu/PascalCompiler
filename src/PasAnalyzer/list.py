from PasAnalyzer.AST import ListNode,AstNode


# --------------------------ListNode-------------------------------------
class ConstExprListNode(ListNode):
    def __init__(self, node):
        super().__init__(node)


class TypeDeclListNode(ListNode):
    def __init__(self, node):
        super().__init__(node)


class FieldDeclListNode(ListNode):
    def __init__(self, node):
        super().__init__(node)


class VarDeclListNode(ListNode):
    def __init__(self, node):
        super().__init__(node)

class ParaDeclListNode(ListNode):
    def __init__(self, node):
        super().__init__(node)


class NameListNode(ListNode):
    def __init__(self, node):
        super().__init__(node)

    def set_type(self, _type_name):
        for var in self.NodeList:
            if var is not None:
                var.var_type = _type_name


class StmtListNode(ListNode):
    def __init__(self, node):
        super().__init__(node)


class CaseExprListNode(ListNode):
    def __init__(self, node):
        super().__init__(node)


class ExprListNode(ListNode):
    def __init__(self, node):
        super().__init__(node)


class ArgsListNode(ListNode):
    def __init__(self, node):
        super().__init__(node)


class RoutineDeclListNode(ListNode):
    def __init__(self, node, _id):
        super().__init__(node)
        self.id = _id
