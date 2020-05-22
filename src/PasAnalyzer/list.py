from PasAnalyzer.AST import AstNode, treenode_tot


# --------------------------ListNode-------------------------------------
class ListNode(AstNode):
    def __init__(self, node=None):
        super().__init__()
        self.NodeList = []
        if node is not None:
            self.NodeList.append(node)

    def append(self, node):
        self.NodeList.append(node)

    def travel(self, indent_num=0):
        print(self.dump(indent_num))
        for o in self.NodeList:
            if o is not None:
                o.travel(indent_num + 2)

    def vis(self, file):
        global treenode_tot
        treenode_tot += 1
        self.cnt = treenode_tot
        for son in self.NodeList:
            if son and isinstance(son, AstNode):
                son.vis(file)
                self.print_link(son, file)
            else:
                if son is self.cnt:
                    continue
                else:
                    self.print_basic(son, file)
        self.print_info(file)


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


class ParaTypeListNode(AstNode):
    def __init__(self, var_list, type):
        super().__init__()
        self.type = type
        self.NodeList = []
        if var_list is not None:
            self.NodeList.append(var_list)

    def append(self, node):
        self.NodeList.append(node)


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
