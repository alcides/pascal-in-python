# PROGRAM HEADING


#start = 'block'

def p_program_start(t):
	'program : header SEMICOLON block DOT'
	pass

def p_header(t):
	'header : PROGRAM IDENTIFIER'
	pass
	
def p_block(t):
	"""block : variable_declaration_part statement_part
	"""
	pass
	
	
def p_variable_declaration_part(t):
	"""variable_declaration_part : VAR variable_declaration_list
	 |
	"""
	pass

def p_variable_declaration_list(t):
	"""variable_declaration_list : variable_declaration_list variable_declaration
	 | variable_declaration
	"""
	# function and procedure missing here
	pass

def p_variable_declaration(t):
	"""variable_declaration : IDENTIFIER COLON type SEMICOLON"""
	pass
	
def p_type(t):
	""" type : TREAL 
	| TINTEGER
	| TCHAR
	| TSTRING """
	pass
	
def p_statement_part(t):
	"""statement_part : BEGIN statement_sequence END"""
	pass
	
def p_statement_sequence(t):
	"""statement_sequence : statement_sequence statement
	 | statement"""
	pass
	
def p_statement(t):
	"""statement : assignment_statement
	 | statement_part
	 | """
	"""
	 | procedure_statement
		
		case_statement
	 | repeat_statement
	 | with_statement
	 | if_statement
	 | while_statement
	 | for_statement
	 |
	"""
	pass
	
def p_assignment_statement(t):
	"""assignment_statement : IDENTIFIER ASSIGNMENT expression"""
	
def p_expression(t):
	"""expression : term
	 | expression sign_weak term"""
	pass

def p_term(t):
	"""term : element 
	| term sign_strong element """
	
	
def p_sign_weak(t):
	"""sign_weak : PLUS
	| MINUS"""
	pass

def p_sign_strong(t):
	"""sign_strong : TIMES
	| DIVISION
	| DIV
	| MOD
	"""
	pass


def p_element(t):
	"""element : IDENTIFIER
	| REAL
	| INTEGER
	| STRING
	| CHAR
	| LPAREN expression RPAREN
	| NOT element
	"""
	pass

def p_error(t):
    print "Syntax error in input, in line %d!" % 0