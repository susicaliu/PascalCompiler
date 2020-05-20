import ply.yacc as yacc
from scanner.lex import tokens

def p_program(p):
    'program : program_head  routine  DOT'
    p[0] = ProgramNode(p[1],p[2])

def p_program_head(p):
    'program_head : PROGRAM  ID  SEMI'
    p[0] = ProgramHeadNode(p[2])

def p_routine(p):
    'routine : routine_head  routine_body'
    p[0] = RoutineNode(p[1],p[2])

def p_sub_routine(p):
    'sub_routine : routine_head  routine_body'
    p[0] = SubRoutineNode(p[1],p[2])

def p_routine_head(p):
    'routine_head : label_part  const_part  type_part  var_part  routine_part'
    p[0] = RoutineHeadNode(p[1],p[2],p[3],p[4],p[5])

def p_label_part(p):
    'label_part : empty'
    p[0] = None

def p_const_part_0(p):
    'const_part : CONST  const_expr_list'
    p[0] = p[2]

def p_const_part_1(p):
    'const_part : empty'
    p[0] = None

def p_const_expr_list_0(p):
    'const_expr_list : const_expr_list  ID  EQUAL  const_value  SEMI'
    p[0] = p[1]
    p[0].append(ConstExprNode(VariableNode(p[2]),p[4]))

def p_const_expr_list_1(p):
    'const_expr_list : ID  EQUAL  const_value  SEMI'
    p[0] = ConstExprListNode(ConstExprNode(p[1],p[3]))

def p_const_value_0(p):
    'const_value : INTEGER'
    p[0] = ConstValueNode('integer',p[1]);

def p_const_value_1(p):
    'const_value : REAL'
    p[0] = ConstValueNode('real',p[1]);

def p_const_value_2(p):
    'const_value : CHAR'
    p[0] = ConstValueNode('char',p[1]);

def p_const_value_3(p):
    'const_value : STRING'
    p[0] = ConstValueNode('string',p[1]);

def p_const_value_4(p):
    'const_value : SYS_CON'
    p[0] = ConstValueNode('syscon',p[1]);###

def p_type_part_0(p):
    'type_part : TYPE type_decl_list'
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
    'type_definition : ID  EQUAL  type_decl  SEMI'
    p[0] = TypeDefinitionNode(p[1],p[3])

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
    p[0] = VariableTypeDeclNode(p[1])

def p_simple_type_decl_2(p):
    'simple_type_decl : LP  name_list  RP '
    p[0] = EnumTypeDeclNode(p[2])

def p_simple_type_decl_3(p):
    'simple_type_decl : const_value  DOTDOT  const_value  '
    p[0] = RangeTypeDeclNode(1,p[1],1,p[3])

def p_simple_type_decl_4(p):
    'simple_type_decl : MINUS  const_value  DOTDOT  const_value'
    p[0] = RangeTypeDeclNode(-1,p[2],1,p[4])

def p_simple_type_decl_5(p):
    'simple_type_decl : MINUS  const_value  DOTDOT  MINUS  const_value'
    p[0] = RangeTypeDeclNode(-1,p[2],-1,p[4])

def p_simple_type_decl_6(p):
    'simple_type_decl : ID  DOTDOT  ID'
    pass###

def p_array_type_decl(p):
    'array_type_decl : ARRAY  LB  simple_type_decl  RB  OF  type_decl'
    p[0] = ArrayTypeDeclNode(p[3],p[6])

def p_record_type_decl(p):
    'record_type_decl : RECORD  field_decl_list  END'
    p[0] = RecordTypeDeclNode(p[2])

def p_field_decl_list_0(p):
    'field_decl_list : field_decl_list  field_decl'
    p[0] = p[1]
    p[0].append(p[2])

def p_field_decl_list_1(p):
    'field_decl_list : field_decl'
    p[0] = FieldDeclListNode(p[1])

def p_field_decl(p):
    'field_decl : name_list  COLON  type_decl  SEMI'
    pass ###

def p_name_list_0(p):
    'name_list : name_list  COMMA  ID'
    p[0] = p[1]
    p[0].append(p[3])

def p_name_list_1(p):
    'name_list : ID'
    p[0] = NameListNode(p[1])

def p_var_part_0(p):
    'var_part : VAR  var_decl_list'
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
    'var_decl :  name_list  COLON  type_decl  SEMI'
    p[0] = VarDeclNode(p[1],p[3])

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
    p[0] = FunctionDeclListNode(p[1]) ###

def p_routine_part_3(p):
    'routine_part : procedure_decl'
    p[0] = ProcedureDeclListNode(p[1]) ###

def p_routine_part_4(p):
    'routine_part : empty'
    p[0] = None

def p_function_decl(p):
    'function_decl : function_head  SEMI  sub_routine  SEMI'
    p[0] = FuntionDeclNode(p[1],p[3])

def p_function_head(p):
    'function_head :  FUNCTION  ID  parameters  COLON  simple_type_decl '
    p[0] = FunctionHeadNode(p[2],p[3],p[5])

def p_procedure_decl(p):
    'procedure_decl :  procedure_head  SEMI  sub_routine  SEMI'
    p[0] = ProcedureDeclNode(p[1],p[3])

def p_procedure_head(p):
    'procedure_head :  PROCEDURE ID parameters '
    p[0] = ProcedureHeadNode(p[2],p[3])

def p_parameters_0(p):
    'parameters : LP  para_decl_list  RP'
    p[0] = p[2]

def p_parameters_1(p):
    'parameters : empty'
    p[0] = None

def p_para_decl_list_0(p):
    'para_decl_list : para_decl_list  SEMI  para_type_list'
    p[0] = p[1]
    p[0].append(p[3])

def p_para_decl_list_1(p):
    'para_decl_list : para_type_list'
    p[0] = ParaDeclListNode(p[1])

def p_para_type_list_0(p):
    'para_type_list : var_para_list COLON  simple_type_decl  '
    p[0] = ParaTypeListNode(p[1],p[3])

def p_para_type_list_1(p):
    'para_type_list : val_para_list  COLON  simple_type_decl'
    p[0] = ParaTypeListNode(p[1],p[3])

def p_var_para_list(p):
    'var_para_list : VAR  name_list'
    p[0] = p[2]

def p_val_para_list(p):
    'val_para_list : name_list'
    p[0] = p[1]

def p_routine_body(p):
    'routine_body : compound_stmt'
    p[0] = p[1]

def p_compound_stmt(p):
    'compound_stmt : BEGIN  stmt_list  END'
    p[0] = p[2]

def p_stmt_list_0(p):
    'stmt_list : stmt_list  stmt  SEMI'
    if p[1] is not None:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = StmtListNode(p[2])

def p_stmt_list_1(p):
    'stmt_list : empty'
    p[0] = None

def p_stmt_0(p):
    'stmt : INTEGER  COLON  non_label_stmt'
    p[0] = p[3]
    p[0].set_id(p[1])###

def p_stmt_1(p):
    'stmt : non_label_stmt'
    p[0] = p[1]

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
    'assign_stmt : ID  ASSIGN  expression'
    p[0] = AssignStmtNode(VariableNode(p[1]),p[3])

def p_assign_stmt_1(p):
    'assign_stmt : ID LB expression RB ASSIGN expression'
    p[0] = AssignStmtNode(ArrayElementNode(p[1],[p[3]]),p[6])

def p_assign_stmt_2(p):
    'assign_stmt : ID  DOT  ID  ASSIGN  expression'
    p[0] = AssignStmtNode(RecordElementNode(p[1],p[3]),p[5]) 

def p_proc_stmt_0(p):
    'proc_stmt : ID'
    p[0] = VariableNode(p[1])

def p_proc_stmt_1(p):
    'proc_stmt : ID  LP  args_list  RP'
    p[0] = CallExprNode(p[1],p[3])

def p_proc_stmt_2(p):
    'proc_stmt : SYS_PROC'
    p[0] = p[1]

def p_proc_stmt_3(p):
    'proc_stmt : SYS_PROC  LP  expression_list  RP'
    p[0] = CallExprNode(p[1],p[3])

def p_proc_stmt_4(p):
    'proc_stmt : READ  LP  factor  RP'
    p[0] = CallExprNode(p[1],p[3])

def p_if_stmt(p):
    'if_stmt : IF  expression  THEN  stmt  else_clause'
    p[0] = IfStmtNode(p[2],p[4],p[5])

def p_else_clause_0(p):
    'else_clause : ELSE stmt'
    p[0] = p[2]

def p_else_clause_1(p):
    'else_clause : empty'
    p[0] = None

def p_repeat_stmt(p):
    'repeat_stmt : REPEAT  stmt_list  UNTIL  expression'
    p[0] = RepeatStmtNode(p[2],p[4])

def p_while_stmt(p):
    'while_stmt : WHILE  expression  DO stmt'
    p[0] = WhileStmtNode(p[2],p[4])

def p_for_stmt(p):
    'for_stmt : FOR  ID  ASSIGN  expression  direction  expression  DO stmt'
    p[0] = ForStmt(p[2],p[4],p[5],p[6],p[8]) ###

def p_direction_0(p):
    'direction : TO'
    p[0] = ConstValueNode('integer',1)

def p_direction_1(p):
    'direction : DOWNTO'
    p[0] = ConstValueNode('integer',-1)

def p_case_stmt(p):
    'case_stmt : CASE expression OF case_expr_list  END'
    p[0] = CaseStmtNode(p[2],p[4])

def p_case_expr_list_0(p):
    'case_expr_list : case_expr_list  case_expr'
    if p[1] is None:
        p[0] = CaseExprListNode(p[2]) ###
    else:
        p[0] = p[1]
        p[0].append(p[2])
    
def p_case_expr_list_1(p):
    'case_expr_list : case_expr'
    p[0] = CaseExprListNode(p[1])

def p_case_expr_0(p):
    'case_expr : const_value  COLON  stmt  SEMI'
    p[0] = CaseExprNode(p[1],p[3])

def p_case_expr_1(p):
    'case_expr : ID  COLON  stmt  SEMI'
    p[0] = CaseExprNode(p[1],p[3])

def p_goto_stmt(p):
    'goto_stmt : GOTO  INTEGER'
    pass###

def p_expression_list_0(p):
    'expression_list : expression_list  COMMA  expression'
    p[0] = p[1]
    if p[3] is not None:
        p[0].append(p[3])

def p_expression_list_1(p):
    'expression_list : expression'
    p[0] = ExprListNode(p[1])

def p_expression_0(p):
    'expression : expression  GE  expr'
    p[0] = BinaryExprNode(p[2],p[1],p[3])

def p_expression_1(p):
    'expression : expression  GT  expr'
    p[0] = BinaryExprNode(p[2],p[1],p[3])

def p_expression_2(p):
    'expression : expression  LE  expr'
    p[0] = BinaryExprNode(p[2],p[1],p[3])

def p_expression_3(p):
    'expression : expression  LT  expr'
    p[0] = BinaryExprNode(p[2],p[1],p[3])

def p_expression_4(p):
    'expression : expression  EQUAL  expr  '
    p[0] = BinaryExprNode(p[2],p[1],p[3])

def p_expression_5(p):
    'expression : expression  UNEQUAL  expr'
    p[0] = BinaryExprNode(p[2],p[1],p[3])

def p_expression_6(p):
    'expression : expr'
    p[0] = p[1]

def p_expr_0(p):
    'expr : expr  PLUS  term'
    p[0] = BinaryExprNode('+',p[1],p[3])

def p_expr_1(p):
    'expr : expr  MINUS  term'
    p[0] = BinaryExprNode('-',p[1],p[3])

def p_expr_2(p):
    'expr : expr  OR  term'
    p[0] = BinaryExprNode('|',p[1],p[3])

def p_expr_3(p):
    'expr : term'
    p[0] = p[1]

def p_term_0(p):
    'term : term  MUL  factor'
    p[0] = BinaryExprNode('*',p[1],p[3])

def p_term_1(p):
    'term : term  DIV  factor'
    p[0] = BinaryExprNode('/',p[1],p[3])

def p_term_2(p):
    'term : term  MOD  factor '
    p[0] = BinaryExprNode('%',p[1],p[3])

def p_term_3(p):
    'term : term  AND  factor'
    p[0] = BinaryExprNode('+',p[1],p[3])

def p_term_4(p):
    'term   : factor'
    p[0] = p[1]

def p_factor_0(p):
    'factor : ID'
    p[0] = VariableNode(p[1])

def p_factor_1(p):
    'factor : ID  LP  args_list  RP'
    p[0] = CallExprNode(p[1],p[3])

def p_factor_2(p):
    'factor : SYS_FUNCT'
    p[0] = CallExprNode(p[1],None)

def p_factor_3(p):
    'factor : SYS_FUNCT  LP  args_list  RP'
    p[0] = CallExprNode(p[1],p[3])

def p_factor_4(p):
    'factor : const_value'
    p[0] = p[1]

def p_factor_5(p):
    'factor : LP  expression  RP'
    p[0] = p[2]

def p_factor_6(p):
    'factor : NOT  factor'
    p[0] = UnaryExprNode('!',p[2])

def p_factor_7(p):
    'factor : MINUS  factor'
    p[0] = UnaryExprNode('-',p[2])

def p_factor_8(p):
    'factor : ID  LB  expression  RB'
    p[0] = ArrayElementNode(p[1],[p[3]])

def p_factor_9(p):
    'factor : ID  DOT  ID'
    p[0] = RecordElementNode(p[1],p[3])

def p_args_list_0(p):
    'args_list : args_list  COMMA  expression'
    p[0] = p[1]
    p[0].append(p[3])

def p_args_list_1(p):
    'args_list : expression'
    p[0] = ArgsListNode(p[1])
    