import ply.lex as lex
import re
from ply.lex import TOKEN

reserved = {
    'and': 'PAS_AND',
    'array': 'PAS_ARRAY',
    'begin': 'PAS_BEGIN',
    'break': 'PAS_BREAK',
    'case': 'PAS_CASE',
    'const': 'PAS_CONST',
    'continue': 'PAS_CONTINUE',
    'default': 'PAS_DEFAULT',
    'div': 'PAS_DIV',
    'do': 'PAS_DO',
    'downto': 'PAS_DOWNTO',
    'else': 'PAS_ELSE',
    'end': 'PAS_END',
    'exit': 'PAS_EXIT',
    'file': 'PAS_FILE',
    'for': 'PAS_FOR',
    'forward': 'PAS_FORWARD',
    'function': 'PAS_FUNCTION',
    'goto': 'PAS_GOTO',
    'if': 'PAS_IF',
    'in': 'PAS_IN',
    'label': 'PAS_LABEL',
    'mod': 'PAS_MOD',
    'nil': 'PAS_NIL',
    'not': 'PAS_NOT',
    'of': 'PAS_OF',
    'or': 'PAS_OR',
    'packed': 'PAS_PACKED',
    'procedure': 'PAS_PROCEDURE',
    'program': 'PAS_PROGRAM',
    'record': 'PAS_RECORD',
    'repeat': 'PAS_REPEAT',
    'set': 'PAS_SET',
    'sizeof': 'PAS_SIZEOF',
    'then': 'PAS_THEN',
    'to': 'PAS_TO',
    'type': 'PAS_TYPE',
    'until': 'PAS_UNTIL',
    'var': 'PAS_VAR',
    'while': 'PAS_WHILE',
    'with': 'PAS_WITH',
    'xor': 'PAS_XOR',
}

sys_funct = ["abs", "chr", "odd", "ord", "pred", "sqr", "sqrt", "succ"]
sys_proc = ["write", "writeln"]
sys_con = ["false", "maxint", "true"]
sys_type = ["boolean", "char", "integer", "real"]

for k in sys_funct:
    reserved[k] = 'SYS_FUNCT'
for k in sys_proc:
    reserved[k] = 'SYS_PROC'
for k in sys_con:
    reserved[k] = 'SYS_CON'
for k in sys_type:
    reserved[k] = 'SYS_TYPE'

sym = ('SYM_ADD', 'SYM_SUB', 'SYM_MUL', 'SYM_DIV', 'SYM_EQ', 'SYM_LT', 'SYM_GT', 'SYM_LBRAC', 'SYM_RBRAC', 'SYM_PERIOD',
       'SYM_COMMA', 'SYM_COLON', 'SYM_SEMICOLON', 'SYM_AT', 'SYM_CARET', 'SYM_LPAREN', 'SYM_RPAREN', 'SYM_NE', 'SYM_LE',
       'SYM_GE', 'SYM_ASSIGN', 'SYM_RANGE')

tokens = ['ID', 'INT', 'REAL', 'CHAR', 'STR', ] + list(sym) + list(set(reserved.values()))


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


t_SYM_ADD = re.escape(r'+')
t_SYM_SUB = re.escape(r'-')
t_SYM_MUL = re.escape(r'*')
t_SYM_DIV = re.escape(r'/')
t_SYM_EQ = re.escape(r'=')
t_SYM_LT = re.escape(r'<')
t_SYM_GT = re.escape(r'>')
t_SYM_LBRAC = re.escape(r'[')
t_SYM_RBRAC = re.escape(r']')
t_SYM_PERIOD = re.escape(r'.')
t_SYM_COMMA = re.escape(r',')
t_SYM_COLON = re.escape(r':')
t_SYM_SEMICOLON = re.escape(r';')
t_SYM_AT = re.escape(r'@')
t_SYM_CARET = re.escape(r'^')
t_SYM_LPAREN = re.escape(r'(')
t_SYM_RPAREN = re.escape(r')')
t_SYM_NE = re.escape(r'<>')
t_SYM_LE = re.escape(r'<=')
t_SYM_GE = re.escape(r'>=')
t_SYM_ASSIGN = re.escape(r':=')
t_SYM_RANGE = re.escape(r'..')

sign = r"'+|-'"
t_INT = r"[0-9]+"
t_REAL = r"([0-9]+\.[0-9]+)|([0-9]+\.[0-9]+e{SIGN}?[0-9]+)|([0-9]+e{SIGN}?[0-9]+)"
t_CHAR = r"'([^']|\")'"
t_STR = r"\'[^']*\'"


# todo:comment identify
# t_COMMENT = r"{'[^\}]*'}"
# t_ESC_CHAR = r"\'\#{INT}\'"

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="parselog.txt",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()
lex.lex(debug=True, debuglog=log)

if __name__ == '__main__':
    import sys

    lexer = lex.lex(debug=1, debuglog=log)
    while True:
        s = input('>>')
        # s=open(sys.argv[1],'r').read()
        lexer.input(s)
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
