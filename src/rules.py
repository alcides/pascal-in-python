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
	"""block : variable_declaration_part statement_part
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
	 | procedure_or_function
	 |
	"""
	if len(t) > 1:
		t[0] = t[1]
	
	
def p_procedure_or_function(t):
	"""procedure_or_function : proc_or_func_declaration SEMICOLON procedure_or_function
		| proc_or_func_declaration SEMICOLON"""
		
	if len(t) == 4:
		t[0] = Node('function_list',t[1],t[2])
	else:
		t[0] = t[1]
		
		
def p_proc_or_func_declaration(t):
	""" proc_or_func_declaration : procedure_declaration
               | function_declaration """
	t[0] = t[1]
		
		
def p_procedure_declaration(t):
	"""procedure_declaration : procedure_heading SEMICOLON block"""
	t[0] = Node("procedure",t[1],t[3])
		
		
def p_procedure_heading(t):
	""" procedure_heading : PROCEDURE IDENTIFIER 
	| PROCEDURE IDENTIFIER parameter_list """
	
	if len(t) == 3:
		t[0] = Node("procedure_head",t[2])
	else:
		t[0] = Node("procedure_head",t[2],t[3])
		
		
def p_function_declaration(t):
	""" function_declaration : function_heading SEMICOLON block"""
	t[0] = Node('function',t[1],t[3])
	
	
def p_function_heading(t):
	""" function_heading : FUNCTION IDENTIFIER
	 	| FUNCTION IDENTIFIER COLON IDENTIFIER
		| FUNCTION IDENTIFIER parameter_list COLON IDENTIFIER"""
	if len(t) == 3:
		t[0] = Node("function_head",t[2])
	elif len(t) == 5:
		t[0] = Node("function_head",t[2],t[3])
	else:
		t[0] = Node("function_head",t[2],t[3],t[5])

def p_parameter_list(t):
	""" parameter_list : LPAREN inside_parameter_list RPAREN"""
	t[0] = t[2]
	
def p_inside_parameter_list(t):
	""" inside_parameter_list : parameter SEMICOLON inside_parameter_list
	| parameter SEMICOLON"""
	if len(t) == 4:
		t[0] = Node("parameter_list", t[1], t[3])
	else:
		t[0] = t[1]
		
def p_parameter(t):
	""" parameter : identifier_list COLON IDENTIFIER
	 	| VAR identifier_list COLON IDENTIFIER
		| procedure_heading
		| function_heading"""
	if len(t) == 2:
		t[0] = t[1]
	elif len(t) == 4:
		t[0] = Node("parameter", t[1],t[3])
	else:
		t[0] = Node("parameter_var", t[2], t[4])

def p_identifier_list(t):
	""" identifier_list : identifier_list COMMA IDENTIFIER
	| IDENTIFIER """
	if len(t)==2:
		t[0] = t[1]
	else:
		t[0] = Node("identifier_list",t[1],t[3])
	
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
	t[0] = t[1]


def p_element(t):
	"""element : IDENTIFIER
	| REAL
	| INTEGER
	| STRING
	| CHAR
	| LPAREN expression RPAREN
	| NOT element
	"""
	if len(t) == 2:
		t[0] = t[1]
	elif len(t) == 3:
		# not e
		t[0] = Node('not',t[2])
	else:
		# ( e )
		t[0] = t[2]

def p_error(t):
	print "Syntax error in input, in line %d!" % 0