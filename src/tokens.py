A = r'[aA]'
B = r'[bB]'
C = r'[cC]'
D = r'[dD]'
E = r'[eE]'
F = r'[fF]'
G = r'[gG]'
H = r'[hH]'
I = r'[iI]'
J = r'[jJ]'
K = r'[kK]'
L = r'[lL]'
M = r'[mM]'
N = r'[nN]'
O = r'[oO]'
P = r'[pP]'
Q = r'[qQ]'
R = r'[rR]'
S = r'[sS]'
T = r'[tT]'
U = r'[uU]'
V = r'[vV]'
W = r'[wW]'
X = r'[xX]'
Y = r'[yY]'
Z = r'[zZ]'
QUOTE = r'(\'|")'


tokens = (

	# main
	'PROGRAM',
	'DOT',
	
	# blocks
	'VAR',
	'BEGIN',
	'END',
	
	# assignment
	'IDENTIFIER',
	'ASSIGNMENT',
	'SEMICOLON',
	
	# functions
	'LPAREN',
	'RPAREN',

	# types
	'REAL',
	'INTEGER',
	'STRING',
	
	#stdlib
	'WRITE',
	'WRITELN'
)


# Regular statement rules for tokens.
t_PROGRAM		= P+R+O+G+R+A+M
t_DOT			= r"\."

t_VAR			= V+A+R
t_BEGIN			= B+E+G+I+N
t_END			= E+N+D

t_IDENTIFIER	= r"[a-zA-Z]([a-zA-Z0-9])+"
t_ASSIGNMENT	= r":="
t_SEMICOLON		= r";"

t_LPAREN		= r"\("
t_RPAREN		= r"\)"

t_REAL			= r"[0-9]+\.[0-9]+"
t_INTEGER		= r"[0-9]+"

t_WRITE			= W+R+I+T+E
t_WRITELN		= W+R+I+T+E+L+N



def t_STRING(t): 
    r'(\"|\')([^\\"]|(\\.))*(\"|\')' 
    escaped = 0 
    str = t.value[1:-1] 
    new_str = "" 
    for i in range(0, len(str)): 
        c = str[i] 
        if escaped: 
            if c == "n": 
                c = "\n" 
            elif c == "t": 
                c = "\t" 
            new_str += c 
            escaped = 0 
        else: 
            if c == "\\": 
                escaped = 1 
            else: 
                new_str += c 
    t.value = new_str 
    return t

def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)





