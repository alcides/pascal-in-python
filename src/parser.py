import sys
from ply import yacc
from tokens import *
from rules import *

# A string containing ignored characters (spaces and tabs).
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]


# Build the lexer
yacc.yacc()


if __name__ == '__main__':
	
	if len(sys.argv) > 1:
		f = open(sys.argv[1],"r")
		data = f.read()
		f.close()
	else:
		data = raw_input()

	yacc.parse(data)