from ast import Node

# META

#start = 'block'

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVISION'),
    ('left', 'DIV', 'MOD'),
    ('left', 'EQ', 'NEQ', 'LTE','LT','GT','GTE'),
    ('left', 'OR', 'AND'),
)


def p_program_start(t):
	'program : header SEMICOLON block DOT'
	t[0] = Node('program',t[1],t[3])

def p_header(t):
	'header : PROGRAM IDENTIFIER'
	t[0] = t[2]
	
def p_block(t):
	"""block : variable_declaration_part procedure_or_function statement_part
	"""
	t[0] = Node('block',t[1],t[2])
	
	
def p_variable_declaration_part(t):
	"""variable_declaration_part : VAR variable_declaration_list
	 |
	"""
	if len(t) > 1:
		t[0] = t[2]

def p_variable_declaration_list(t):
	"""variable_declaration_list : variable_declaration variable_declaration_list
	 | variable_declaration
	"""
	# function and procedure missing here
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Node('var_list',t[1],t[2])

def p_variable_declaration(t):
	"""variable_declaration : IDENTIFIER COLON type SEMICOLON"""
	t[0] = Node('var',t[1],t[3])
	
	
	
def p_procedure_or_function(t):
	"""procedure_or_function : proc_or_func_declaration SEMICOLON procedure_or_function
		| """
		
	if len(t) == 4:
		t[0] = Node('function_list',t[1],t[2])
		
		
def p_proc_or_func_declaration(t):
	""" proc_or_func_declaration : procedure_declaration
               | function_declaration """
	t[0] = t[1]
		
		
def p_procedure_declaration(t):
	"""procedure_declaration : procedure_heading SEMICOLON block"""
	t[0] = Node("procedure",t[1],t[3])
		
		
def p_procedure_heading(t):
	""" procedure_heading : PROCEDURE IDENTIFIER 
	| PROCEDURE IDENTIFIER LPAREN parameter_list RPAREN"""
	
	if len(t) == 3:
		t[0] = Node("procedure_head",t[2])
	else:
		t[0] = Node("procedure_head",t[2],t[4])
		
		
def p_function_declaration(t):
	""" function_declaration : function_heading SEMICOLON block"""
	t[0] = Node('function',t[1],t[3])
	
	
def p_function_heading(t):
	""" function_heading : FUNCTION type
	 	| FUNCTION IDENTIFIER COLON type
		| FUNCTION IDENTIFIER LPAREN parameter_list RPAREN COLON type"""
	if len(t) == 3:
		t[0] = Node("function_head",t[2])
	elif len(t) == 5:
		t[0] = Node("function_head",t[2],t[3])
	else:
		t[0] = Node("function_head",t[2],t[4],t[7])

	
def p_parameter_list(t):
	""" parameter_list : parameter COMMA parameter_list
	| parameter"""
	if len(t) == 4:
		t[0] = Node("parameter_list", t[1], t[3])
	else:
		t[0] = t[1]
		
def p_parameter(t):
	""" parameter : IDENTIFIER COLON type"""
	t[0] = Node("parameter", t[1], t[3])

def p_type(t):
	""" type : TREAL 
	| TINTEGER
	| TCHAR
	| TSTRING """
	t[0] = Node('type',t[1])
	
def p_statement_part(t):
	"""statement_part : BEGIN statement_sequence END"""
	t[0] = t[2]
	
def p_statement_sequence(t):
	"""statement_sequence : statement SEMICOLON statement_sequence
	 | statement"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Node('statement_list',t[1],t[3])
	
def p_statement(t):
	"""statement : assignment_statement
	 | statement_part
	 | if_statement
	 | while_statement
	 | repeat_statement
	 | for_statement
	 | procedure_or_function_call
	 |
	"""
	if len(t) > 1:
		t[0] = t[1]
	
	
def p_procedure_or_function_call(t):
	""" procedure_or_function_call : IDENTIFIER LPAREN param_list RPAREN
	| IDENTIFIER """
	
	if len(t) == 2:
		t[0] = Node("function_call", t[1])
	else:
		t[0] = Node("function_call",t[1],t[3])

def p_param_list(t):
	""" param_list : param_list COMMA param
	 | param """
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Node("parameter_list",t[1],t[3])

def p_param(t):
	""" param : expression """
	t[0] = Node("parameter",t[1])

	
def p_if_statement(t):
	"""if_statement : IF expression THEN statement ELSE statement
	| IF expression THEN statement
	"""
	
	if len(t) == 5:
		t[0] = Node('if',t[2],t[4])
	else:
		t[0] = Node('ifelse',t[2],t[4],t[6])
	
def p_while_statement(t):
	"""while_statement : WHILE expression DO statement"""
	t[0] = Node('while',t[2],t[4])
	
	
def p_repeat_statement(t):
	"""repeat_statement : REPEAT statement UNTIL expression"""
	t[0] = Node('repeat',t[2],t[4])
	
def p_for_statement(t):
	"""for_statement : FOR assignment_statement TO expression DO statement
	| FOR assignment_statement DOWNTO expression DO statement
	"""
	t[0] = Node('for',t[2],t[3],t[4],t[6])
	
def p_assignment_statement(t):
	"""assignment_statement : IDENTIFIER ASSIGNMENT expression"""
	t[0] = Node('assign',t[1],t[2])
	
def p_expression(t):
	"""expression : element
	 | expression sign element"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Node('op',t[1],t[2],t[3])

def p_sign(t):
	"""sign : PLUS
	| MINUS
	| TIMES
	| DIVISION
	| DIV
	| MOD
	| AND
	| OR
	| EQ
	| NEQ
	| LT
	| LTE
	| GT
	| GTE
	"""
	t[0] = Node('sign',t[1])


def p_element(t):
	"""element : IDENTIFIER
	| REAL
	| INTEGER
	| STRING
	| CHAR
	| LPAREN expression RPAREN
	| NOT element
	| function_call_inline
	"""
	if len(t) == 2:
		t[0] = t[1]
	elif len(t) == 3:
		# not e
		t[0] = Node('not',t[2])
	else:
		# ( e )
		t[0] = Node('element',t[2])
		
def p_function_call_inline(t):
	""" function_call_inline : IDENTIFIER param_list"""
	t[0] = Node('function_call_inline',t[1],t[2])
	

def p_error(t):
	print "Syntax error in input, in line %d!" % t.lineno