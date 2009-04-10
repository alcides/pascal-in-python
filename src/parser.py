import sys
from ply import yacc,lex
from tokens import *
from rules import *


# Build the lexer
yacc.yacc()


if __name__ == '__main__':
	
	if len(sys.argv) > 1:
		f = open(sys.argv[1],"r")
		data = f.read()
		f.close()
	else:
		data = ""
		while True:
			try:
				data = raw_input()
			except:
				break

	yacc.parse(data,lexer = lex.lex())