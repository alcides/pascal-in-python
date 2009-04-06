__globals = {}

# PROGRAM HEADING

def p_program_start(t):
	'program : header SEMICOLON block DOT'
	pass

def p_header(t):
	'header : PROGRAM IDENTIFIER'
	pass
	
def p_block(t):
	"""block : variable_declaration_part
	 procedure_and_function_declaration_part
	 statement_part
	"""
	pass
	
	
def p_variable_declaration_part(t):
	"""VAR variable_declaration_list
	 |
	"""
	pass

def p_variable_declaration_list(t):
	"""variable_declaration_list : variable_declaration_list variable_declaration
	 | variable_declaration
	"""
	pass

def p_variable_declaration(t):
	"""variable_declaration : IDENTIFIER COLON type SEMICOLON"""
	pass
	
def p_type(t):
	""" type : TREAL | TINTEGER | TCHAR | TSTRING """
	pass
	
def p_procedure_and_function_declaration_part(t):
	"""""" # TODO
	pass
	
def p_statement_part(t):
	"""statement_part : BEGIN statement_sequence END"""
	pass
	
def p_statement_sequence(t):
	"""statement_sequence : statement_sequence statement
	 | statement"""
	pass
	
def p_statement(t):
	"""statement : open_statement
	 | closed_statement"""
	pass
	
def p_open_statement(t):
	"""open_statement : open_with_statement
	 | open_if_statement
	 | open_while_statement
	 | open_for_statement
	"""
	pass
	
def p_closed_statement(t):
	"""closed_statement : assignment_statement
	 | procedure_statement
	 | compound_statement
	 | case_statement
	 | repeat_statement
	 | closed_with_statement
	 | closed_if_statement
	 | closed_while_statement
	 | closed_for_statement
	 |
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
	if t[1] in __globals:
		__globals[t[1]][1] = t[3]
	else:
		raise TypeError("Variable %s not defined." % (t[1],))
	
def p_statement_plus(t) :
    'statement : statement PLUS statement'
    t[0] = t[1] + t[3]


def p_error(t):
    print "Syntax error in input!"