import sys

sys.path.append("..")
from PasAnalyzer.AST import *
from PasAnalyzer.expr import *
from PasAnalyzer.rout import *
from PasAnalyzer.list import *
from PasAnalyzer.stmt import *
from PasAnalyzer.type import *
from PasAnalyzer.vari import *

from PasParser.parser import *

from gentable import GenTable
import llvmlite.ir as ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_double, c_int, c_void_p, cast, c_int32
from random import randint


def wirte(data):
    print(data)


def read():
    data = int(input())
    return data


class CodeGenerator(object):
    def __init__(self, module_name):
        self.module = ir.Module(module_name)
        self.GenTable = GenTable()
        self.scope_id = 0

    def generate(self, ast_node):
        return self._codegen_(ast_node, None)

    def add_new_variable(self, variable, variable_type, builder):
        with builder.goto_entry_block():
            typ = self.type_convert(variable_type)
            address = builder.alloca(typ, size=None, name=variable)
            self.GenTable.add_variable(variable_name=variable, address=address, variable_type=typ,
                                       scope_id=self.scope_id)
        return address

    def _codegen_(self, ast_node, builder):
        if (ast_node is None):
            return
        # print(ast_node.__class__.__name__)
        return getattr(self, '_codegen_' + ast_node.__class__.__name__)(ast_node, builder)

    def register_writeln(self):
        write_type = ir.FunctionType(ir.VoidType(), (ir.IntType(32),))
        c_write_type = CFUNCTYPE(c_void_p, c_int32)
        c_write = c_write_type(wirte)
        write_address = cast(c_write, c_void_p).value

        write_func_type = ir.FunctionType(ir.VoidType(), (ir.IntType(32),))
        write_func = ir.Function(self.module, write_func_type, 'writeln')
        builder = ir.IRBuilder(write_func.append_basic_block('entry'))
        write_f = builder.inttoptr(ir.Constant(ir.IntType(64), write_address),
                                   write_func_type.as_pointer(), name='write_f')
        arg = write_func.args[0]
        arg.name = 'arg0'
        call = builder.call(write_f, [arg])
        builder.ret_void()

        self.GenTable.add_function(func_name='writeln', func_block=write_func, scope_id=self.scope_id)

    def register_readln(self):
        read_type = ir.FunctionType(ir.VoidType(), (ir.IntType(32),))
        c_read_type = CFUNCTYPE(c_void_p, c_int32)
        c_read = c_read_type(wirte)
        read_address = cast(c_read, c_void_p).value

        read_func_type = ir.FunctionType(ir.VoidType(), (ir.IntType(32),))
        read_func = ir.Function(self.module, read_func_type, 'readln')
        builder = ir.IRBuilder(read_func.append_basic_block('entry'))
        read_f = builder.inttoptr(ir.Constant(ir.IntType(64), read_address),
                                  read_func_type.as_pointer(), name='read_f')
        arg = read_func.args[0]
        arg.name = 'arg0'
        call = builder.call(read_f, [arg])
        builder.ret_void()

        self.GenTable.add_function(func_name='readln', func_block=read_func, scope_id=self.scope_id)

    def _codegen_ProgramNode(self, ast_node, builder):
        self.register_writeln()
        self.register_readln()

        global_func_type = ir.FunctionType(ir.VoidType(), ())
        self.global_func = ir.Function(self.module, global_func_type, 'global_func')

        builder = ir.IRBuilder(self.global_func.append_basic_block('global_block'))

        if (ast_node.routine):
            self._codegen_(ast_node.routine, builder)
        builder.ret_void()

    # ---------------------------------RoutineNode-------------------------
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

    # ---------------------------------VariableNode-------------------------
    def _codegen_VariableNode(self, ast_node, builder):
        # id
        variable_addr = self.GenTable.get_address(ast_node.id)
        return builder.load(variable_addr, name=ast_node.id)

    def _codegen_ArrayElementNode(self, ast_node, builder):
        # id  expression_array
        variable_addr = self.GenTable.get_address(ast_node.id)
        vairable_type = self.type_convert(ast_node.type)
        array_index = []

        for index in ast_node.expression_array:
            if isinstance(index, VariableNode):
                val = self._codegen_(index, builder)
            else:
                val = ir.Constant(ir.IntType(32), index.value)
            array_index.append(val)
        array_index.append(ir.Constant(ir.IntType(32), 0))
        address = builder.gep(variable_addr, array_index)
        return builder.load(address, "array_element")

    def _codegen_RecordElementNode(self, ast_node, builder):
        # id id2
        variable_addr = self.GenTable.get_address(ast_node.id + '.' + ast_node.id2)  ####todo
        return builder.load(variable_addr, name=ast_node.id2)

    def _codegen_ConstExprNode(self, ast_node, builder):
        # id const_value
        variable = self.add_new_variable(variable=ast_node.id, variable_type=ast_node.const_value.type, builder=builder)
        value = self._codegen_(ast_node.const_value, builder)
        return builder.store(value, variable)

    # --------------------------TypeNode-------------------------------------
    def _codegen_TypeDefinitionNode(self, ast_node, builder):
        # id type_decl
        variable = ast_node.id.id
        type = self._codegen_(ast_node.type_decl, builder)
        # print(variable)
        self.GenTable.add_type(variable_name=variable, variable_type=type, scope_id=self.scope_id)

    def _codegen_ConstValueNode(self, ast_node, builder):
        # type value
        return ir.Constant(self.type_convert(ast_node.type), ast_node.value)

    def _codegen_FunctionProto(self, proto, builder, func_para_name, func_para_type, func_return_type_list, gen_type):
        func_name = proto.id.id
        if (gen_type == 'function'):
            func_return_type = self.type_convert(proto.simple_type_decl.id)
        else:
            func_return_type = self.type_convert('void')
        if (proto.parameters):
            for para_type_list in proto.parameters.NodeList:
                type = self.type_convert(para_type_list.type.id)
                func_para_type += [type] * len(para_type_list.NodeList[0].NodeList)
                func_para_name += [var.id for var in para_type_list.NodeList[0].NodeList]

        func_type = ir.FunctionType(func_return_type, func_para_type)
        func = ir.Function(self.module, func_type, func_name)
        func_return_type_list.append(func_return_type)
        return func

    def _codegen_FunctionDeclNode(self, ast_node, builder):
        # function_head sub_routine
        gen_type = 'function'
        self.scope_id += 1
        func_para_name = []
        func_para_type = []
        func_return_type_list = []
        proto = self._codegen_FunctionProto(proto=ast_node.function_head, builder=builder,
                                            func_para_name=func_para_name, func_para_type=func_para_type,
                                            func_return_type_list=func_return_type_list, gen_type=gen_type)
        func_name = ast_node.function_head.id.id
        self.GenTable.add_function(func_name, proto, self.scope_id)

        func_enrty = proto.append_basic_block('entry')
        Builder = ir.IRBuilder(block=func_enrty)
        for index, arg in enumerate(proto.args):
            arg.name = func_para_name[index]
            address = self.add_new_variable(variable=arg.name, variable_type=func_para_type[index], builder=Builder)
            Builder.store(arg, address)
        func_return_type = func_return_type_list[0]
        return_address = self.add_new_variable(variable=func_name, variable_type=func_return_type, builder=Builder)
        res = self._codegen_(ast_node.sub_routine, Builder)

        return_value = Builder.load(ptr=return_address, name=func_name)
        Builder.ret(return_value)

        self.GenTable.delete_scope(self.scope_id)
        self.scope_id -= 1
        return proto

    def _codegen_ProcedureDeclNode(self, ast_node, builder):
        # function_head sub_routine
        gen_type = 'Procedure'
        self.scope_id += 1
        func_para_name = []
        func_para_type = []
        func_return_type_list = []
        proto = self._codegen_FunctionProto(proto=ast_node.function_head, builder=builder,
                                            func_para_name=func_para_name, func_para_type=func_para_type,
                                            func_return_type_list=func_return_type_list, gen_type=gen_type)
        func_name = ast_node.function_head.id
        self.GenTable.add_function(func_name, proto, self.scope_id)

        func_enrty = proto.append_basic_block('entry')
        Builder = ir.IRBuilder(block=func_enrty)
        for index, arg in enumerate(proto.args):
            arg.name = func_para_name[index]
            address = self.add_new_variable(variable=arg.name, variable_type=func_para_type[index], builder=Builder)
            Builder.store(arg, address)
        func_return_type = func_return_type_list[0]
        return_address = self.add_new_variable(variable=func_name, variable_type=func_return_type, builder=Builder)
        res = self._codegen_(ast_node.sub_routine, Builder)

        Builder.ret_void()

        self.GenTable.delete_scope(self.scope_id)
        self.scope_id -= 1
        return proto

    def _codegen_SimpleTypeDeclNode(self, ast_node, builder):
        # type_name
        type = self.type_convert(ast_node.id)  ####自定义type不能这样写
        return type

    def _codegen_VariableTypeDeclNode(self, ast_node, builder):
        # id
        type = self.type_convert(ast_node.id.type)
        return type

    def _codegen_ArrayTypeDeclNode(self, ast_node, builder):
        # simple_type_decl type_decl
        range_type = self._codegen_(ast_node.simple_type_decl, builder)
        element_type = self._codegen_(ast_node.type_decl, builder)
        array_len = range_type[1] - range_type[0] + 1
        ret = ir.ArrayType(element_type, array_len)
        return ret

    def _codegen_EnumTypeDeclNode(self, ast_node, builder):
        # name_list
        type = self.type_convert(ast_node.name_list.type)

        return type

    def _codegen_RecordTypeDeclNode(self, ast_node, builder):
        # field_decl_list
        type = self.type_convert(ast_node.field_decl_list.type)
        return type

    def _codegen_RangeTypeDeclNode(self, ast_node, builder):
        # const_value1 const_value2
        num1 = ast_node.const_value1.value
        num2 = ast_node.const_value2.value
        return [int(num1), int(num2)]

    def _codegen_VarDeclNode(self, ast_node, builder):
        # name_list type_decl
        for name in ast_node.name_list.NodeList:
            if (isinstance(ast_node.type_decl, VariableTypeDeclNode)):
                type = self.GenTable.get_type(ast_node.type_decl.id)
                address = self.add_new_variable(variable=name.id, variable_type=type, builder=builder)
            else:
                # print(name.id, ast_node.type_decl.id)
                address = self.add_new_variable(variable=name.id, variable_type=ast_node.type_decl.id, builder=builder)

        return address

    def _codegen_FieldDeclNode(self, ast_node, builder):
        # name_list type_decl
        for name in ast_node.name_list.NodeList:

            if (isinstance(ast_node.type_decl, VariableTypeDeclNode)):
                type = self.type_convert(ast_node.type_decl.id)
                address = self.add_new_variable(variable=name.id, variable_type=type, builder=builder)
            else:
                address = self.add_new_variable(variable=name.id, variable_type=ast_node.type_decl.id, builder=builder)

        return address

    # -----------------------------------StmtNode-------------------------------------
    def _codegen_StmtNode(self, node, builder):
        return self._codegen_(node.stmt_node, builder)

    def _codegen_AssignStmtNode(self, node, builder):
        lhs = self.GenTable.get_address(node.element_node)
        rhs = self._codegen_(node.expression, builder)
        if rhs.type != lhs.type.pointee:
            rhs = builder.load(rhs)
        builder.store(rhs, lhs)

    def _codegen_IfStmtNode(self, node, builder):
        pred = builder.icmp_signed('!=', self._codegen_(node.expression, builder), ir.Constant(ir.IntType(1), 0))
        with builder.if_else(pred) as (then, otherwise):
            with then:
                self._codegen_(node.stmt, builder)
            with otherwise:
                self._codegen_(node.else_clause, builder)

    def _codegen_RepeatStmtNode(self, node, builder):
        ran = str(randint(0, 0x7FFFFFFF))

        repeat_block = builder.append_basic_block("repeat_" + ran)
        stmt = builder.append_basic_block("stmt_" + ran)
        jumpout = builder.append_basic_block("jumpout_" + ran)

        builder.branch(repeat_block)

        r_builder = ir.IRBuilder(repeat_block)
        s_builder = ir.IRBuilder(stmt)
        self._codegen_(node.stmt_list, s_builder)
        end_expr = self._codegen_(node.expression, r_builder)
        end_cond = builder.icmp_signed('==', end_expr, ir.Constant(ir.IntType(1), 0))
        r_builder.cbranch(end_cond, repeat_block, jumpout)
        s_builder.branch(repeat_block)

        builder.position_at_end(jumpout)

    def _codegen_WhileStmtNode(self, node, builder):
        ran = str(randint(0, 0x7FFFFFFF))

        while_block = builder.append_basic_block("while_" + ran)
        stmt = builder.append_basic_block("stmt_" + ran)
        jumpout = builder.append_basic_block("jumpout_" + ran)

        builder.branch(while_block)

        w_builder = ir.IRBuilder(while_block)
        s_builder = ir.IRBuilder(stmt)
        end_expr = self._codegen_(node.expression, w_builder)
        end_cond = builder.icmp_signed('==', end_expr, ir.Constant(ir.IntType(1), 0))
        w_builder.cbranch(end_cond, while_block, jumpout)
        self._codegen_(node.stmt, s_builder)
        s_builder.branch(while_block)

        builder.position_at_end(jumpout)

    def _codegen_ForStmtNode(self, node, builder):

        var_addr = self.add_new_variable(variable=node.name.id, variable_type=ir.IntType(32), builder=builder)
        init_val = self._codegen_(node.expression1, builder)

        final_val =self._codegen_(node.expression2, builder)

        direction = node.direction.value  # int--> TO:1, DOWNTO: -1
        builder.store(init_val, var_addr)

        ran = str(randint(0, 0x7FFFFFFF))

        for_block = builder.append_basic_block("for_" + ran)
        f_builder = ir.IRBuilder(for_block)
        stmt = f_builder.append_basic_block("stmt_" + ran)
        jumpout = f_builder.append_basic_block("jumpout_" + ran)

        builder.branch(for_block)

        if direction == 1:
            cmp = ">"
        elif direction == -1:
            cmp = "<"
        cond = f_builder.icmp_signed(cmp, init_val, final_val)
        f_builder.cbranch(cond, jumpout, stmt)
        s_builder = ir.IRBuilder(stmt)
        self._codegen_(node.stmt, s_builder)
        if direction == 1:
            current_val = s_builder.add(init_val, ir.IntType(32)(1))
        elif direction == -1:
            current_val = s_builder.sub(init_val, ir.IntType(32)(1))
        s_builder.store(current_val, var_addr)
        s_builder.branch(for_block)

        builder.position_at_end(jumpout)

    def _codegen_CaseStmtNode(self, node, builder):
        ran = str(randint(0, 0x7FFFFFFF))

        expr = self._codegen_(node.expression, builder)
        case_expr_list = self._codegen_(node.case_expr_list, builder)
        default = builder.append_basic_block('default_' + ran)

        case_part = builder.switch(expr, default)
        for val, block in case_expr_list:
            case_part.add_case(val, block)
            c_builder = ir.IRBuilder(block)
            c_builder.position_at_end(block)
            c_builder.branch(default)

        builder.position_at_end(default)

    def _codegen_GotoStmtNode(self, node, builder):
        block_id = node.num
        builder.goto_block("goto_" + block_id)

    def _codegen_CallStmtNode(self, node, builder):
        fn = self.GenTable.get_func(node.func_name)
        args = []
        for arg in node.args_list.NodeList:
            if (isinstance(arg, ConstValueNode)):
                args.append(self._codegen_(arg, builder))
            else:
                address = self.GenTable.get_variable_addr(arg)
                arg = builder.load(address)
                args.append(arg)
        # args = [self._codegen_(arg, builder) for arg in node.args_list.NodeList]
        return builder.call(fn, args, 'call_fn')

    # ---------------------------------ExpressionNode-------------------------
    def _codegen_BinaryExprNode(self, ast_node, builder):
        # >= > <= < = <> + - | * / % &
        ret = None
        if ast_node.op == '>=':
            ret = self._codegen_CompExpr(ast_node, builder)
        elif ast_node.op == '>':
            ret = self._codegen_CompExpr(ast_node, builder)
        elif ast_node.op == '<=':
            ret = self._codegen_CompExpr(ast_node, builder)
        elif ast_node.op == '<':
            ret = self._codegen_CompExpr(ast_node, builder)
        elif ast_node.op == '==':
            ret = self._codegen_CompExpr(ast_node, builder)
        elif ast_node.op == '!=':
            ret = self._codegen_CompExpr(ast_node, builder)
        elif ast_node.op == '+':
            ret = self._codegen_AddExpr(ast_node, builder)
        elif ast_node.op == '-':
            ret = self._codegen_SubExpr(ast_node, builder)
        elif ast_node.op == '|':
            ret = self._codegen_OrExpr(ast_node, builder)
        elif ast_node.op == '*':
            ret = self._codegen_MulExpr(ast_node, builder)
        elif ast_node.op == '/':
            ret = self._codegen_DivExpr(ast_node, builder)
        elif ast_node.op == '%':
            ret = self._codegen_ModExpr(ast_node, builder)
        elif ast_node.op == '&':
            ret = self._codegen_AndExpr(ast_node, builder)
        else:
            pass  ####error
        return ret

    def _type_cast(self, lhs, rhs):
        if lhs.type == 'real' or rhs.type == 'real':
            return 'real'
        else:
            return 'int'

    def _codegen_CompExpr(self, ast_node, builder):
        ret = None
        type = None
        if (isinstance(ast_node.lexpr, str)):
            lhs = self.GenTable.get_address(ast_node.lexpr)
            lhs = builder.load(lhs)
            addr, type = self.GenTable.get_variable_addr_type(ast_node.lexpr)

        else:
            lhs = self._codegen_(ast_node.lexpr, builder)
            type = lhs.type
        if (isinstance(ast_node.rexpr, str)):
            rhs = self.GenTable.get_address(ast_node.rexpr)
            rhs = builder.load(rhs)
        else:

            rhs = self._codegen_(ast_node.rexpr, builder)
        if isinstance(type, ir.IntType):
            ret = builder.icmp_signed(ast_node.op, lhs, rhs)
        elif isinstance(type, ir.DoubleType):
            ret = builder.fcmp_signed(ast_node.op, lhs, rhs)
        else:
            pass  ####error

        return ret

    def _codegen_AddExpr(self, ast_node, builder):
        ret = None
        type=None

        if (isinstance(ast_node.lexpr, str)):
            lhs = self.GenTable.get_address(ast_node.lexpr)
            lhs = builder.load(lhs)
            addr, type = self.GenTable.get_variable_addr_type(ast_node.lexpr)

        else:
            lhs = self._codegen_(ast_node.lexpr, builder)
            type = lhs.type
        if (isinstance(ast_node.rexpr, str)):
            rhs = self.GenTable.get_address(ast_node.rexpr)
            rhs = builder.load(rhs)
        else:

            rhs = self._codegen_(ast_node.rexpr, builder)

        if isinstance(type, ir.IntType):
            ret = builder.add(lhs, rhs)
        elif isinstance(type,ir.DoubleType):

            ret = builder.fadd(lhs, rhs)
        else:
            pass  ####error
        return ret

    def _codegen_SubExpr(self, ast_node, builder):
        ret = None
        type = None
        if (isinstance(ast_node.lexpr, str)):
            lhs = self.GenTable.get_address(ast_node.lexpr)
            lhs = builder.load(lhs)
            addr, type = self.GenTable.get_variable_addr_type(ast_node.lexpr)

        else:
            lhs = self._codegen_(ast_node.lexpr, builder)
            type = lhs.type
        if (isinstance(ast_node.rexpr, str)):
            rhs = self.GenTable.get_address(ast_node.rexpr)
            rhs = builder.load(rhs)
        else:

            rhs = self._codegen_(ast_node.rexpr, builder)
        if isinstance(type, ir.IntType):
            ret = builder.sub(lhs, rhs)
        elif isinstance(type, ir.DoubleType):
            ret = builder.fsub(lhs, rhs)
        else:
            pass
        return ret

    def _codegen_OrExpr(self, ast_node, builder):
        ret = None
        type = None
        if (isinstance(ast_node.lexpr, str)):
            lhs = self.GenTable.get_address(ast_node.lexpr)
            lhs = builder.load(lhs)
            addr, type = self.GenTable.get_variable_addr_type(ast_node.lexpr)

        else:
            lhs = self._codegen_(ast_node.lexpr, builder)
            type = lhs.type
        if (isinstance(ast_node.rexpr, str)):
            rhs = self.GenTable.get_address(ast_node.rexpr)
            rhs = builder.load(rhs)
        else:

            rhs = self._codegen_(ast_node.rexpr, builder)
        if isinstance(type, ir.IntType):
            ret = builder.or_(lhs, rhs)
        else:
            pass  ####error
        return ret

    def _codegen_MulExpr(self, ast_node, builder):
        ret = None
        type = None
        if (isinstance(ast_node.lexpr, str)):
            lhs = self.GenTable.get_address(ast_node.lexpr)
            lhs = builder.load(lhs)
            addr, type = self.GenTable.get_variable_addr_type(ast_node.lexpr)

        else:
            lhs = self._codegen_(ast_node.lexpr, builder)
            type = lhs.type
        if (isinstance(ast_node.rexpr, str)):
            rhs = self.GenTable.get_address(ast_node.rexpr)
            rhs = builder.load(rhs)
        else:

            rhs = self._codegen_(ast_node.rexpr, builder)
        if isinstance(type, ir.IntType):
            ret = builder.mul(lhs, rhs)
        elif isinstance(type, ir.DoubleType):
            ret = builder.fmul(lhs, rhs)
        else:
            pass  ####error
        return ret

    def _codegen_DivExpr(self, ast_node, builder):
        ret = None
        type = None
        if (isinstance(ast_node.lexpr, str)):
            lhs = self.GenTable.get_address(ast_node.lexpr)
            lhs = builder.load(lhs)
            addr, type = self.GenTable.get_variable_addr_type(ast_node.lexpr)

        else:
            lhs = self._codegen_(ast_node.lexpr, builder)
            type = lhs.type
        if (isinstance(ast_node.rexpr, str)):
            rhs = self.GenTable.get_address(ast_node.rexpr)
            rhs = builder.load(rhs)
        else:

            rhs = self._codegen_(ast_node.rexpr, builder)
        if isinstance(type, ir.IntType):
            ret = builder.sdiv(lhs, rhs)
        elif isinstance(type, ir.DoubleType):
            ret = builder.fdiv(lhs, rhs)
        else:
            pass  ####error
        return ret

    def _codegen_ModExpr(self, ast_node, builder):
        ret = None
        type = None
        if (isinstance(ast_node.lexpr, str)):
            lhs = self.GenTable.get_address(ast_node.lexpr)
            lhs = builder.load(lhs)
            addr, type = self.GenTable.get_variable_addr_type(ast_node.lexpr)

        else:
            lhs = self._codegen_(ast_node.lexpr, builder)
            type = lhs.type
        if (isinstance(ast_node.rexpr, str)):
            rhs = self.GenTable.get_address(ast_node.rexpr)
            rhs = builder.load(rhs)
        else:

            rhs = self._codegen_(ast_node.rexpr, builder)
        if isinstance(type, ir.IntType):
            ret = builder.srem(lhs, rhs)
        elif isinstance(type, ir.DoubleType):
            ret = builder.frem(lhs, rhs)
        else:
            pass  ####error
        return ret

    def _codegen_AndExpr(self, ast_node, builder):
        ret = None
        type = None
        if (isinstance(ast_node.lexpr, str)):
            lhs = self.GenTable.get_address(ast_node.lexpr)
            lhs = builder.load(lhs)
            addr, type = self.GenTable.get_variable_addr_type(ast_node.lexpr)

        else:
            lhs = self._codegen_(ast_node.lexpr, builder)
            type = lhs.type
        if (isinstance(ast_node.rexpr, str)):
            rhs = self.GenTable.get_address(ast_node.rexpr)
            rhs = builder.load(rhs)
        else:

            rhs = self._codegen_(ast_node.rexpr, builder)
        if isinstance(type, ir.IntType):
            ret = builder.and_(lhs, rhs)
        else:
            pass  ####error
        return ret

    def _codegen_ConstExprNode(self, ast_node, builder):
        ret = None
        lhs = self._codegen_(ast_node.id, builder)
        rhs = self._codegen_(ast_node.const_value, builder)
        ret = builder.store(rhs, lhs)
        return ret

    def _codegen_CaseExprNode(self, ast_node, builder):
        ret = None
        rand = randint(0, 0x7FFFFFFF)
        val = self._codegen_(ast_node.const_value, builder)
        tmp_block = builder.append_basic_block('case_' + str(rand))
        tmp_builder = ir.IRBuilder(tmp_block)
        self._codegen_(ast_node.stmt, tmp_builder)
        return val, tmp_block  ####

    def _codegen_UnaryExprNode(self, ast_node, builder):
        ret = None
        val = self._codegen_(ast_node.factor, builder)
        if ast_node.op == '!':
            ret = builder.not_(val)
        elif ast_node.op == '-':
            ret = builder.neg(val)
        else:
            pass  ####error
        return ret

    # --------------------------ListNode-------------------------------------
    def _codegen_ListNode(self, ast_node, builder):
        ret = None
        for son in ast_node.NodeList:
            if son in ast_node.NodeList:
                if son is not None:
                    ret = self._codegen_(son, builder)
        return ret

    def _codegen_ConstExprListNode(self, ast_node, builder):
        ret = self._codegen_ListNode(ast_node, builder)
        return ret

    def _codegen_TypeDeclListNode(self, ast_node, builder):
        ret = self._codegen_ListNode(ast_node, builder)
        return ret

    def _codegen_FieldDeclListNode(self, ast_node, builder):
        ret = self._codegen_ListNode(ast_node, builder)
        return ret

    def _codegen_VarDeclListNode(self, ast_node, builder):
        ret = self._codegen_ListNode(ast_node, builder)
        return ret

    def _codegen_ParaTypeListNode(self, ast_node, builder):
        ret = self._codegen_ListNode(ast_node, builder)
        return ret

    def _codegen_ParaDeclListNode(self, ast_node, builder):
        ret = self._codegen_ListNode(ast_node, builder)
        return ret

    def _codegen_NameListNode(self, ast_node, builder):
        ret = self._codegen_ListNode(ast_node, builder)
        return ret

    def _codegen_StmtListNode(self, ast_node, builder):
        ret = self._codegen_ListNode(ast_node, builder)
        return ret

    def _codegen_CaseExprListNode(self, ast_node, builder):
        ret = []
        for case_expr in ast_node.NodeList:
            val, tmp_block = self._codegen_(case_expr, builder)
            ret.append((val, tmp_block))
        return ret

    def _codegen_ExprListNode(self, ast_node, builder):
        ret = self._codegen_ListNode(ast_node, builder)
        return ret

    def _codegen_ArgsListNode(self, ast_node, builder):
        ret = self._codegen_ListNode(ast_node, builder)
        return ret

    def _codegen_RoutineDeclListNode(self, ast_node, builder):
        ret = self._codegen_ListNode(ast_node, builder)
        return ret

    def type_convert(self, type):
        if (isinstance(type, ir.Type)):
            return type
        if (type in ['integer', 'int']):
            return ir.IntType(32)
        if (type in ['real']):
            return ir.DoubleType()
        if (type in ['boolean','bool']):
            return ir.IntType(1)
        if (type in ['void']):
            return ir.VoidType()
        if (type in ['char']):
            return ir.IntType(8)
        raise Exception('Error: invalid data type')
