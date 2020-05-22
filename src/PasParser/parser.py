import ply.yacc as yacc
import os
from PasScanner.lex import tokens, log
from PasAnalyzer.AST import *
from PasAnalyzer.expr import *
from PasAnalyzer.rout import *
from PasAnalyzer.list import *
from PasAnalyzer.stmt import *
from PasAnalyzer.type import *
from PasAnalyzer.vari import *


def p_program(p):
    'program : program_head  routine  SYM_PERIOD'
    p[0] = ProgramNode(p[1], p[2])


def p_program_head(p):
    'program_head : PAS_PROGRAM  ID  SYM_SEMICOLON'
    p[0] = p[2]


def p_routine(p):
    'routine : routine_head  routine_body'
    p[0] = RoutineNode(p[1], p[2])


def p_sub_routine(p):
    'sub_routine : routine_head  routine_body'
    p[0] = SubRoutineNode(p[1], p[2])


def p_routine_head(p):
    'routine_head : label_part  const_part  type_part  var_part  routine_part'
    p[0] = RoutineHeadNode(p[1], p[2], p[3], p[4], p[5])


########################Label Part########################
def p_label_part(p):
    'label_part : empty'
    p[0] = None


########################Const Part########################
def p_const_part_0(p):
    'const_part : PAS_CONST  const_expr_list'
    p[0] = p[2]


def p_const_part_1(p):
    'const_part : empty'
    p[0] = None


def p_const_expr_list_0(p):
    'const_expr_list : const_expr_list  ID  SYM_EQ  const_value  SYM_SEMICOLON'
    p[0] = p[1]
    p[0].append(ConstExprNode(p[2], p[4]))  ### ConstID


def p_const_expr_list_1(p):
    'const_expr_list : ID  SYM_EQ  const_value  SYM_SEMICOLON'
    p[0] = ConstExprListNode(ConstExprNode(p[1], p[3]))  ### constID


def p_const_value_0(p):
    'const_value : INT'
    p[0] = ConstValueNode('int', p[1]);


def p_const_value_1(p):
    'const_value : REAL'
    p[0] = ConstValueNode('real', p[1]);


def p_const_value_2(p):
    'const_value : CHAR'
    p[0] = ConstValueNode('char', p[1]);


def p_const_value_3(p):
    'const_value : STR'
    p[0] = ConstValueNode('str', p[1]);


def p_const_value_4(p):
    'const_value : SYS_CON'
    p[0] = ConstValueNode('syscon', p[1]);


########################Type Part########################
def p_type_part_0(p):
    'type_part : PAS_TYPE type_decl_list'
    p[0] = p[2]


def p_type_part_1(p):
    'type_part : empty'
    p[0] = None


def p_type_decl_list_0(p):
    'type_decl_list : type_decl_list  type_definition'
    p[0] = p[1]
    p[0].append(p[2])


def p_type_decl_list_1(p):
    'type_decl_list : type_definition'
    p[0] = TypeDeclListNode(p[1])


def p_type_definition(p):
    'type_definition : ID  SYM_EQ  type_decl  SYM_SEMICOLON'
    p[0] = TypeDefinitionNode(p[1], p[3])  ### ConstID


def p_type_decl_0(p):
    'type_decl : simple_type_decl'
    p[0] = p[1]


def p_type_decl_1(p):
    'type_decl : array_type_decl'
    p[0] = p[1]


def p_type_decl_2(p):
    'type_decl : record_type_decl'
    p[0] = p[1]


def p_simple_type_decl_0(p):
    'simple_type_decl : SYS_TYPE'
    p[0] = SimpleTypeDeclNode(p[1])


def p_simple_type_decl_1(p):
    'simple_type_decl : ID'
    p[0] = VariableTypeDeclNode(p[1])  ###


def p_simple_type_decl_2(p):
    'simple_type_decl : SYM_LPAREN  name_list  SYM_RPAREN '
    p[0] = EnumTypeDeclNode(p[2])


def p_simple_type_decl_3(p):
    'simple_type_decl : const_value  SYM_RANGE  const_value  '
    p[0] = RangeTypeDeclNode(1, p[1], 1, p[3])


def p_simple_type_decl_4(p):
    'simple_type_decl : SYM_SUB  const_value  SYM_RANGE  const_value'
    p[0] = RangeTypeDeclNode(-1, p[2], 1, p[4])


def p_simple_type_decl_5(p):
    'simple_type_decl : SYM_SUB  const_value  SYM_RANGE  SYM_SUB  const_value'
    p[0] = RangeTypeDeclNode(-1, p[2], -1, p[4])


def p_simple_type_decl_6(p):
    'simple_type_decl : ID  SYM_RANGE  ID'
    p[0] = RangeTypeDeclNode(1, p[1], 1, p[3])  ###constvaluenode select


def p_array_type_decl(p):
    'array_type_decl : PAS_ARRAY  SYM_LBRAC  simple_type_decl  SYM_RBRAC  PAS_OF  type_decl'
    p[0] = ArrayTypeDeclNode(p[3], p[6])
    ###ERROR simple_type_decl可能有问题


def p_record_type_decl(p):
    'record_type_decl : PAS_RECORD  field_decl_list  PAS_END'
    p[0] = RecordTypeDeclNode(p[2])


def p_field_decl_list_0(p):
    'field_decl_list : field_decl_list  field_decl'
    p[0] = p[1]
    p[0].append(p[2])


def p_field_decl_list_1(p):
    'field_decl_list : field_decl'
    p[0] = FieldDeclListNode(p[1])


def p_field_decl(p):
    'field_decl : name_list  SYM_COLON  type_decl  SYM_SEMICOLON'
    p[0] = FieldDeclNode(p[1], p[3])


def p_name_list_0(p):
    'name_list : name_list  SYM_COMMA  ID'
    p[0] = p[1]
    p[0].append(p[3])


def p_name_list_1(p):
    'name_list : ID'
    p[0] = NameListNode(p[1])


###############################Var Part###########################
def p_var_part_0(p):
    'var_part : PAS_VAR  var_decl_list'
    p[0] = p[2]


def p_var_part_1(p):
    'var_part : empty'
    p[0] = None


def p_var_decl_list_0(p):
    'var_decl_list : var_decl_list  var_decl'
    p[0] = p[1]
    p[0].append(p[2])


def p_var_decl_list_1(p):
    'var_decl_list : var_decl'
    p[0] = VarDeclListNode(p[1])


def p_var_decl(p):
    'var_decl :  name_list  SYM_COLON  type_decl  SYM_SEMICOLON'
    p[0] = VarDeclNode(p[1], p[3])


############################Function & Procedure part####################
def p_routine_part_0(p):
    'routine_part : routine_part  function_decl'
    p[0] = p[1]
    p[0].append(p[2])


def p_routine_part_1(p):
    'routine_part : routine_part  procedure_decl'
    p[0] = p[1]
    p[0].append(p[2])


def p_routine_part_2(p):
    'routine_part : function_decl'
    p[0] = RoutineDeclListNode(p[1], 'func')


def p_routine_part_3(p):
    'routine_part : procedure_decl'
    p[0] = RoutineDeclListNode(p[1], 'proc')


def p_routine_part_4(p):
    'routine_part : empty'
    p[0] = None


def p_function_decl(p):
    'function_decl : function_head  SYM_SEMICOLON  sub_routine  SYM_SEMICOLON'
    p[0] = FunctionDeclNode(p[1], p[3])


def p_function_head(p):
    'function_head :  PAS_FUNCTION  ID  parameters  SYM_COLON  simple_type_decl '
    p[0] = FunctionHeadNode(p[2], p[3], p[5])


def p_procedure_decl(p):
    'procedure_decl :  procedure_head  SYM_SEMICOLON  sub_routine  SYM_SEMICOLON'
    p[0] = ProcedureDeclNode(p[1], p[3])


def p_procedure_head(p):
    'procedure_head : PAS_PROCEDURE ID parameters '
    p[0] = ProcedureHeadNode(p[2], p[3])


def p_parameters_0(p):
    'parameters : SYM_LPAREN  para_decl_list  SYM_RPAREN'
    p[0] = p[2]


def p_parameters_1(p):
    'parameters : empty'
    p[0] = None


def p_para_decl_list_0(p):
    'para_decl_list : para_decl_list  SYM_SEMICOLON  para_type_list'
    p[0] = p[1]
    p[0].append(p[3])


def p_para_decl_list_1(p):
    'para_decl_list : para_type_list'
    p[0] = ParaDeclListNode(p[1])


def p_para_type_list_0(p):
    'para_type_list : var_para_list SYM_COLON simple_type_decl  '
    p[0] = ParaTypeListNode(p[1], p[3])


def p_para_type_list_1(p):
    'para_type_list : val_para_list  SYM_COLON  simple_type_decl'
    p[0] = ParaTypeListNode(p[1], p[3])


def p_var_para_list(p):
    'var_para_list : PAS_VAR  name_list'
    p[0] = p[2]


def p_val_para_list(p):
    'val_para_list : name_list'
    p[0] = p[1]


#############################Body Part############################
def p_routine_body(p):
    'routine_body : compound_stmt'
    p[0] = p[1]


def p_compound_stmt(p):
    'compound_stmt : PAS_BEGIN  stmt_list  PAS_END'
    p[0] = p[2]


def p_stmt_list_0(p):
    'stmt_list : stmt_list  stmt  SYM_SEMICOLON'
    if p[1] is not None:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = StmtListNode(p[2])


def p_stmt_list_1(p):
    'stmt_list : empty'
    p[0] = None


def p_stmt_0(p):
    'stmt : INT  SYM_COLON  non_label_stmt'
    p[0] = StmtNode(p[3], p[1])


def p_stmt_1(p):
    'stmt : non_label_stmt'
    p[0] = StmtNode(p[1], None)


def p_non_label_stmt_0(p):
    'non_label_stmt : assign_stmt'
    p[0] = p[1]


def p_non_label_stmt_1(p):
    'non_label_stmt : proc_stmt'
    p[0] = p[1]


def p_non_label_stmt_2(p):
    'non_label_stmt : compound_stmt'
    p[0] = p[1]


def p_non_label_stmt_3(p):
    'non_label_stmt : if_stmt'
    p[0] = p[1]


def p_non_label_stmt_4(p):
    'non_label_stmt : repeat_stmt'
    p[0] = p[1]


def p_non_label_stmt_5(p):
    'non_label_stmt : while_stmt '
    p[0] = p[1]


def p_non_label_stmt_6(p):
    'non_label_stmt : for_stmt'
    p[0] = p[1]


def p_non_label_stmt_7(p):
    'non_label_stmt : case_stmt'
    p[0] = p[1]


def p_non_label_stmt_8(p):
    'non_label_stmt : goto_stmt'
    p[0] = p[1]


def p_assign_stmt_0(p):
    'assign_stmt : ID  SYM_ASSIGN  expression'
    p[0] = AssignStmtNode(VariableNode(p[1]), p[3])


def p_assign_stmt_1(p):
    'assign_stmt : ID SYM_LBRAC expression SYM_RBRAC SYM_ASSIGN expression'
    p[0] = AssignStmtNode(ArrayElementNode(p[1], [p[3]]), p[6])


def p_assign_stmt_2(p):
    'assign_stmt : ID  SYM_PERIOD  ID  SYM_ASSIGN  expression'
    p[0] = AssignStmtNode(RecordElementNode(p[1], p[3]), p[5])


def p_proc_stmt_0(p):
    'proc_stmt : ID'
    p[0] = CallStmtNode(p[1], None)  ###


def p_proc_stmt_1(p):
    'proc_stmt : ID  SYM_LPAREN  args_list  SYM_RPAREN'
    p[0] = CallStmtNode(p[1], p[3])


def p_proc_stmt_2(p):
    'proc_stmt : SYS_PROC'
    p[0] = p[1]


def p_proc_stmt_3(p):
    'proc_stmt : SYS_PROC  SYM_LPAREN  expression_list  SYM_RPAREN'
    p[0] = CallStmtNode(p[1], p[3])


def p_proc_stmt_4(p):
    'proc_stmt : PAS_READ  SYM_LPAREN  factor  SYM_RPAREN'
    p[0] = CallStmtNode(p[1], p[3])  ###factor must be id


def p_if_stmt(p):
    'if_stmt : PAS_IF  expression  PAS_THEN  stmt  else_clause'
    p[0] = IfStmtNode(p[2], p[4], p[5])


def p_else_clause_0(p):
    'else_clause : PAS_ELSE stmt'
    p[0] = p[2]


def p_else_clause_1(p):
    'else_clause : empty'
    p[0] = None


def p_repeat_stmt(p):
    'repeat_stmt : PAS_REPEAT  stmt_list  PAS_UNTIL  expression'
    p[0] = RepeatStmtNode(p[2], p[4])


def p_while_stmt(p):
    'while_stmt : PAS_WHILE  expression  PAS_DO stmt'
    p[0] = WhileStmtNode(p[2], p[4])


def p_for_stmt(p):
    'for_stmt : PAS_FOR  ID  SYM_ASSIGN  expression  direction  expression PAS_DO stmt'
    p[0] = ForStmtNode(p[2], p[4], p[5], p[6], p[8])  ###


def p_direction_0(p):
    'direction : PAS_TO'
    p[0] = ConstValueNode('int', 1)


def p_direction_1(p):
    'direction : PAS_DOWNTO'
    p[0] = ConstValueNode('int', -1)


def p_case_stmt(p):
    'case_stmt : PAS_CASE expression PAS_OF case_expr_list  PAS_END'
    p[0] = CaseStmtNode(p[2], p[4])


def p_case_expr_list_0(p):
    'case_expr_list : case_expr_list  case_expr'
    if p[1] is None:
        p[0] = CaseExprListNode(p[2])  ###
    else:
        p[0] = p[1]
        p[0].append(p[2])


def p_case_expr_list_1(p):
    'case_expr_list : case_expr'
    p[0] = CaseExprListNode(p[1])


def p_case_expr_0(p):
    'case_expr : const_value  SYM_COLON  stmt  SYM_SEMICOLON'
    p[0] = CaseExprNode(p[1], p[3])


def p_case_expr_1(p):
    'case_expr : ID  SYM_COLON  stmt  SYM_SEMICOLON'
    p[0] = CaseExprNode(p[1], p[3])


def p_goto_stmt(p):
    'goto_stmt : PAS_GOTO  INT'
    p[0] = GotoStmtNode(p[2]);
    pass  ###


def p_expression_list_0(p):
    'expression_list : expression_list  SYM_COMMA  expression'
    p[0] = p[1]
    if p[3] is not None:
        p[0].append(p[3])


def p_expression_list_1(p):
    'expression_list : expression'
    p[0] = ExprListNode(p[1])


def p_expression_0(p):
    'expression : expression  SYM_GE  expr'
    p[0] = BinaryExprNode(p[2], p[1], p[3])


def p_expression_1(p):
    'expression : expression  SYM_GT  expr'
    p[0] = BinaryExprNode(p[2], p[1], p[3])


def p_expression_2(p):
    'expression : expression  SYM_LE  expr'
    p[0] = BinaryExprNode(p[2], p[1], p[3])


def p_expression_3(p):
    'expression : expression  SYM_LT  expr'
    p[0] = BinaryExprNode(p[2], p[1], p[3])


def p_expression_4(p):
    'expression : expression  SYM_EQ  expr  '
    p[0] = BinaryExprNode(p[2], p[1], p[3])


def p_expression_5(p):
    'expression : expression  SYM_NE  expr'
    p[0] = BinaryExprNode(p[2], p[1], p[3])


def p_expression_6(p):
    'expression : expr'
    p[0] = p[1]


def p_expr_0(p):
    'expr : expr  SYM_ADD  term'
    p[0] = BinaryExprNode('+', p[1], p[3])


def p_expr_1(p):
    'expr : expr  SYM_SUB  term'
    p[0] = BinaryExprNode('-', p[1], p[3])


def p_expr_2(p):
    'expr : expr  PAS_OR  term'
    p[0] = BinaryExprNode('|', p[1], p[3])


def p_expr_3(p):
    'expr : term'
    p[0] = p[1]


def p_term_0(p):
    'term : term  SYM_MUL  factor'
    p[0] = BinaryExprNode('*', p[1], p[3])


def p_term_1(p):
    'term : term  SYM_DIV  factor'
    p[0] = BinaryExprNode('/', p[1], p[3])


def p_term_2(p):
    'term : term  PAS_MOD  factor '
    p[0] = BinaryExprNode('%', p[1], p[3])


def p_term_3(p):
    'term : term  PAS_AND  factor'
    p[0] = BinaryExprNode('+', p[1], p[3])


def p_term_4(p):
    'term   : factor'
    p[0] = p[1]


def p_factor_0(p):
    'factor : ID'
    p[0] = VariableNode(p[1])


def p_factor_1(p):
    'factor : ID  SYM_LPAREN  args_list  SYM_RPAREN'
    p[0] = CallStmtNode(p[1], p[3])


def p_factor_2(p):
    'factor : SYS_FUNCT'
    p[0] = CallStmtNode(p[1], None)


def p_factor_3(p):
    'factor : SYS_FUNCT  SYM_LPAREN  args_list  SYM_RPAREN'
    p[0] = CallStmtNode(p[1], p[3])


def p_factor_4(p):
    'factor : const_value'
    p[0] = p[1]


def p_factor_5(p):
    'factor : SYM_LPAREN  expression  SYM_RPAREN'
    p[0] = p[2]


def p_factor_6(p):
    'factor : PAS_NOT  factor'
    p[0] = UnaryExprNode('!', p[2])


def p_factor_7(p):
    'factor : SYM_SUB  factor'
    p[0] = UnaryExprNode('-', p[2])


def p_factor_8(p):
    'factor : ID  SYM_LBRAC  expression  SYM_RBRAC'
    p[0] = ArrayElementNode(p[1], [p[3]])


def p_factor_9(p):
    'factor : ID  SYM_PERIOD  ID'
    p[0] = RecordElementNode(p[1], p[3])


def p_args_list_0(p):
    'args_list : args_list  SYM_COMMA  expression'
    p[0] = p[1]
    p[0].append(p[3])


def p_args_list_1(p):
    'args_list : expression'
    p[0] = ArgsListNode(p[1])


def p_empty(p):
    'empty : '
    p[0] = None


parser = yacc.yacc()

try:
    s = input('calc > ')
except EOFError:
    print('Error')

result = parser.parse(s)
visible = True
print(result)
if visible:
    f = open('parsetree.dot', 'w')
    f.write('digraph g {\n')
    result.vis(f)
    f.write('}\n')
    f.close()
    os.system('dot -Tpng parsetree.dot -o parsetree.png')
else:
    result.travle()
