__globals = {}

# PROGRAM HEADING

def p_program_start(t):
	'program : header SEMICOLON block DOT'
	pass

def p_header(t):
	'header : PROGRAM IDENTIFIER'
	pass
	
def p_block(t):
	"""block : type_definition_part
	 variable_declaration_part
	 procedure_and_function_declaration_part
	 statement_part
	"""
	pass
	
def p_sign(t):
	"""sign : PLUS
	| MINUS
	| TIMES
	| DIVISION
	| DIV
	| MOD
	"""
	pass



def p_assign_statement(t) :
	'assign_statement : IDENTIFIER ASSIGNMENT statement'
	__globals[t[1]] = t[3]
	
def p_statement_plus(t) :
    'statement : statement PLUS statement'
    t[0] = t[1] + t[3]


def p_error(t):
    print "Syntax error in input!"