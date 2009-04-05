QUOTE = r'(\'|")'


tokens = (

	# assignment
	'IDENTIFIER',
	'ASSIGNMENT',
	'SEMICOLON',
	'COLON',

	'COMMENT',

	# main
	'PROGRAM',
	'DOT',
	
	# blocks
	'VAR',
	'BEGIN',
	'END',
	
	# control flow
	'IF',
	'THEN',
	'ELSE',
	
	# operations
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVISION',
	'DIV',
	'MOD',
	
	# comparations
	'EQ',
	'NEQ',
	'LT',
	'GT',
	'LTE',
	'GTE',
	
	# functions
	'LPAREN',
	'RPAREN',
	'PROCEDURE',
	'FUNCTION',

	# types
	'REAL',
	'INTEGER',
	'STRING',
	'CHAR',
	
	# types names
	'TREAL',
	'TINTEGER',
	'TSTRING',
	'TCHAR',
	
	#stdlib
	'WRITE',
	'WRITELN'
)


# Regular statement rules for tokens.
t_DOT			= r"\."

t_ASSIGNMENT	= r":="
t_SEMICOLON		= r";"
t_COLON			= r":"

t_PLUS			= r"\+"
t_MINUS			= r"\-"
t_TIMES			= r"\*"
t_DIVISION		= r"\\"

t_EQ			= r"\="
t_NEQ			= r"\<\>"
t_LT			= r"\<"
t_GT			= r"\>"
t_LTE			= r"\<\="
t_GTE			= r"\>\="


t_LPAREN		= r"\("
t_RPAREN		= r"\)"

t_REAL			= r"(\-)*[0-9]+\.[0-9]+"
t_INTEGER		= r"(\-)*[0-9]+"


reserved_keywords = {
	'program':	'PROGRAM',
	'var':		'VAR',
	'begin':	'BEGIN',
	'end':		'END',
	'if':		'IF',
	'then':		'THEN',
	'else':		'ELSE',
	'div':		'DIV',
	'mod':		'MOD',
	'procedure':'PROCEDURE',
	'function':	'FUNCTION'
}

def t_IDENTIFIER(t):
	r"[a-zA-Z]([a-zA-Z0-9])*"
	if t.value.lower() in reserved_keywords:
		t.type = reserved_keywords[t.value.lower()]
	return t


def t_CHAR(t):
	r"(\'([^\\\'])\')|(\"([^\\\"])\")"
	return t

def t_STRING(t): 
    r"(\"([^\\\"]|(\\.))*\")|(\'([^\\\']|(\\.))*\')"
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



def t_COMMENT(t):
	r"{[^}]*}"

def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)





