treenode_tot = 0
basic_tot = 0
class AstNode(object):
    def __init__(self):
        super().__init__()
        self.cnt = 0

    def gattrs(self):
        return [i for i in dir(self) if not callable(getattr(self, i)) and not i.startswith('__')]

    def travel(self, indent_num=0):
        print(self.dump(indent_num))
        attrs = self.gattrs()
        for o in attrs:
            v = getattr(self, o)
            if v and isinstance(v, AstNode):
                v.travel(indent_num + 2)    

    def dump(self, indent_num=0):
        return '{0}{1}'.format(
            ' ' * indent_num, self.__class__.__name__)
        
    def vis(self, file):
        global treenode_tot
        treenode_tot += 1
        self.cnt = treenode_tot
        attrs = self.gattrs()
        for o in attrs:
            son = getattr(self, o)
            if son and isinstance(son, AstNode):
                son.vis(file)
                self.print_link(son,file)
            else:
                if son is self.cnt:
                    continue
                else:
                   self.print_basic(son,file)
        self.print_info(file)

    def print_info(self,file):
        file.write('TN'+str(self.cnt)+'[shape=oval, label='+self.__class__.__name__+'];\n')
    
    def print_link(self,v,file):
        file.write('TN'+str(self.cnt)+'->TN'+str(v.cnt)+';\n')

    def print_basic(self,v,file):
        if v is None:
            return
        global basic_tot
        basic_tot += 1
        file.write('TN'+str(self.cnt)+'->BS'+str(basic_tot)+';\n')
        file.write('BS'+str(basic_tot)+'[shape=oval,label='+str(v)+'];\n')

class ProgramNode(AstNode):
    def __init__(self, program_head, routine):
        super().__init__()
        self.routine = routine
        self.program_head = program_head