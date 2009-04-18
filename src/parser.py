import sys
from ply import yacc,lex
from tokens import *
from rules import *
from builder import *

def get_input():
	if len(sys.argv) > 1:
		f = open(sys.argv[1],"r")
		data = f.read()
		f.close()
	else:
		data = ""
		while True:
			try:
				data += raw_input() + "\n"
			except:
				break
	return data

def main():
	yacc.yacc()
	data = get_input()
	ast =  yacc.parse(data,lexer = lex.lex())	
	o = Writer()(ast)
	
if __name__ == '__main__':
	main()