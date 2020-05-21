import sys
sys.path.append("..")
from PasAnalyzer.AST import *
from PasAnalyzer.expr import *
from PasAnalyzer.rout import *
from PasAnalyzer.list import *
from PasAnalyzer.stmt import *
from PasAnalyzer.type import *
from PasAnalyzer.vari import *

from gentable import GenTable
import llvmlite.ir as ir
import llvmlite.binding as llvm
class CodeGenerator(object):
    def __init__(self, module_name):
        self.module = ir.Module(module_name)
        self.builder = None
        self.GenTable = GenTable()
        self.scope_id = 0

    def generate(self, ast):
        pass

    def type_convert(self,type):
        if(isinstance(type,ir.Type)):
            return type
        if(type in ['integer','int']):
            return ir.IntType(32)
        if (type in ['real']):
            return ir.DoubleType()
        if (type in ['boolean']):
            return ir.IntType(1)
        if (type in ['void']):
            return ir.VoidType()
        if (type in ['char']):
            return ir.IntType(8)
        raise Exception('Error: invalid data type')

    def add_new_variable(self,variable,variable_type,builder):
        with builder.goto_entry_block():
            typ=self.type_convert(variable_type)
            address=builder.alloca(typ, size=None, name=variable)
            self.GenTable.add_variable(variable_name=variable,address=address,variable_type=typ,scope_id=self.scope_id)
        return address

    def assign(self,variable,value,builder):
        # Store value to pointer ptr.
        return builder.store(variable,value)

    def _codegen_(self, ast_node, builder):
        if (ast_node is None):
            return
        return getattr(self, '_codegen_' + ast_node.__class__.__name__)(ast_node, builder)

    def _codegen_ProgramNode(self, ast_node, builder):
        # TODO  program_head  routine
        pass

    def _codegen_RoutineNode(self, ast_node, builder):
        # routine_head routine_body
        res = None
        if (ast_node.routine_head):
            res = self._codegen_(ast_node.routine_head, builder)
        if (ast_node.routine_body):
            res = self._codegen_(ast_node.routine_body, builder)

        return res

    def _codegen_SubRoutineNode(self, ast_node, builder):
        # routine_head routine_body
        res = None
        if (ast_node.routine_head):
            temp = self._codegen_(ast_node.routine_head, builder)
            if (temp):
                res = temp
        if (ast_node.routine_body):
            temp = self._codegen_(ast_node.routine_body, builder)
            if (temp):
                res = temp

        return res

    def _codegen_RoutineHeadNode(self, ast_node, builder):
        # label_part const_part type_part var_part routine_part
        res = None
        if (ast_node.label_part):
            temp = self._codegen_(ast_node.label_part, builder)
            if (temp):
                res = temp
        if (ast_node.const_part):
            temp = self._codegen_(ast_node.const_part, builder)
            if (temp):
                res = temp
        if (ast_node.type_part):
            temp = self._codegen_(ast_node.type_part, builder)
            if (temp):
                res = temp
        if (ast_node.var_part):
            temp = self._codegen_(ast_node.var_part, builder)
            if (temp):
                res = temp
        if (ast_node.routine_part):
            temp = self._codegen_(ast_node.routine_part, builder)
            if (temp):
                res = temp

        return res

    def _codegen_VariableNode(self,ast_node,builder):
        #id
        variable_addr=self.GenTable.get_variable_addr(ast_node.id)
        return builder.load(variable_addr, name=ast_node.id)

    def _codegen_ArrayElementNode(self,ast_node,builder):
        # id  expression_array
        variable_addr,vairable_type=self.GenTable.get_variable_addr_type(ast_node.id)
        array_index=[]
        for index in ast_node.expression_array:
            if isinstance(index,VariableNode):
                val=self._codegen_(index,builder)
            else:
                val=builder.constant(ir.IntType(32),index.value)
            array_index.append(val)
        array_index.append(builder.constant(ir.IntType(32),0))
        address=builder.gep(variable_addr,array_index)
        return builder.load(address,"array_element")

    def _codegen_RecordElementNode(self,ast_node,builder):
        #id id2
        variable_addr= self.GenTable.get_record_variable_addr(ast_node.id,ast_node.id2)
        return builder.load(variable_addr, name=ast_node.id2)
    def _codegen_ConstExprNode(self,ast_node,builder):
        #id const_value
        variable=self.add_new_variable(variable=ast_node.id,variable_type=ast_node.const_value.type,builder=builder)
        value=self._codegen_(ast_node.const_value,builder)
        return self.assign(variable=variable,value=value,builder=builder)
    def _codegen_TypeDefinitionNode(self,ast_node,builder):
        #id type_decl
        variable=ast_node.id
        type=self._codegen_(ast_node.type_decl,builder)
        self.GenTable.add_type(variable_name=variable,variable_type=type,scope_id=self.scope_id)

    def _codegen_ConstValueNode(self, ast_node, builder):
        # type value
        return builder.constant(self.type_convert(ast_node.type),ast_node.value)

    def _codegen_VarDeclNode(self, ast_node, builder):
        # name_list type_decl
        for name in ast_node.name_list.NodeList:
            if(isinstance(ast_node.type_decl,VariableTypeDeclNode)):
                type=self.GenTable.get_type(ast_node.type_decl.id)
                address=self.add_new_variable(variable=name,variable_type=type,builder=builder)
            else:
                address = self.add_new_variable(variable=name, variable_type=ast_node.type_decl.id, builder=builder)

        return address

    def _codegen_FieldDeclNode(self, ast_node, builder):
        # name_list type_decl
        for name in ast_node.name_list.NodeList:
            if (isinstance(ast_node.type_decl, VariableTypeDeclNode)):
                type = self.GenTable.get_type(ast_node.type_decl.id)
                address = self.add_new_variable(variable=name, variable_type=type, builder=builder)
            else:
                address = self.add_new_variable(variable=name, variable_type=ast_node.type_decl.id, builder=builder)

        return address
    def _codegen_FunctionProto(self,proto,builder,func_para_name,func_para_type,func_return_type_list,gen_type):
        func_name=proto.id
        if(gen_type=='function'):
            func_return_type = self.type_convert(proto.simple_type_decl.type_name )
        else:
            func_return_type = self.type_convert('void')
        if(proto.parameters):
            for para_type_list in proto.parameters.NodeList:
                type=self.type_convert(para_type_list.type.type_name)
                func_para_type+=type*len(para_type_list.NodeList[0].NodeList)
                func_para_name+=para_type_list.NodeList[0].NodeList

        func_type=ir.FunctionType(func_return_type,func_para_type)
        func=ir.Function(self.module,func_type,func_name)
        func_return_type_list.append(func_return_type)
        return func


    def _codegen_FunctionDeclNode(self,ast_node,builder):
        #function_head sub_routine
        gen_type='function'
        self.scope_id+=1
        func_para_name=[]
        func_para_type=[]
        func_return_type_list=[]
        proto=self._codegen_FunctionProto(proto=ast_node.function_head,builder=builder,
                                          func_para_name=func_para_name,func_para_type=func_para_type,
                                          func_return_type_list=func_return_type_list,gen_type=gen_type)
        func_name=ast_node.function_head.id
        self.GenTable.add_function(func_name,proto,self.scope_id)

        func_enrty=proto.append_basic_block('entry')
        Builder=ir.IRBuilder(block=func_enrty)
        for index,arg in enumerate(proto.args):
            arg.name=func_para_name[index]
            address=self.add_new_variable(variable=arg.name,variable_type=func_para_type[index],builder=Builder)
            Builder.store(arg,address)
        func_return_type=func_return_type_list[0]
        return_address = self.add_new_variable(variable=func_name, variable_type=func_return_type, builder=Builder)
        res=self._codegen_(ast_node.sub_routine,Builder)

        return_value=Builder.load(ptr=return_address,name=func_name)
        Builder.ret(return_value)

        self.GenTable.delete_scope(self.scope_id)
        self.scope_id-=1
        return proto

    def _codegen_ProcedureDeclNode(self,ast_node,builder):
        #function_head sub_routine
        gen_type='function'
        self.scope_id+=1
        func_para_name=[]
        func_para_type=[]
        func_return_type_list=[]
        proto=self._codegen_FunctionProto(proto=ast_node.function_head,builder=builder,
                                          func_para_name=func_para_name,func_para_type=func_para_type,
                                          func_return_type_list=func_return_type_list,gen_type=gen_type)
        func_name=ast_node.function_head.id
        self.GenTable.add_function(func_name,proto,self.scope_id)

        func_enrty=proto.append_basic_block('entry')
        Builder=ir.IRBuilder(block=func_enrty)
        for index,arg in enumerate(proto.args):
            arg.name=func_para_name[index]
            address=self.add_new_variable(variable=arg.name,variable_type=func_para_type[index],builder=Builder)
            Builder.store(arg,address)
        func_return_type=func_return_type_list[0]
        return_address = self.add_new_variable(variable=func_name, variable_type=func_return_type, builder=Builder)
        res=self._codegen_(ast_node.sub_routine,Builder)

        Builder.ret_void()

        self.GenTable.delete_scope(self.scope_id)
        self.scope_id-=1
        return proto

    def _codegen_CaseExprNode(self,ast_node,builder):
        pass

    def _codegen_BinaryExprNode(self,ast_node,builder):
        if ast_node.op == ':=':
            pass