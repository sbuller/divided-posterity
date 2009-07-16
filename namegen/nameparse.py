# -*- coding: utf-8 -*-

tokens = (
	'CODE',
	'NUMBER',
	'TEXT',
	'IDENTIFIER'
)

def name_lexer():
	import ply.lex as lex
	states = ( ('literal','exclusive'),
	           ('var','exclusive')
	         )

	literals = "()%?|&"

	def t_begin_literal(t):
		r'{'
		t.lexer.begin('literal')
	def t_literal_end(t):
		r'}'
		t.lexer.begin('INITIAL')
	t_literal_TEXT = r'[a-zA-Z\']+'

	def t_literal_error(t):
		print "Illegal literal character '%s'" % t.value[0]

	def t_begin_var(t):
		r'[[]'
		t.lexer.begin('var')
	def t_var_end(t):
		r'[]]'
		t.lexer.begin('INITIAL')
	t_var_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_-]*'

	def t_var_error(t):
		print "Illegal literal character '%s'" % t.value[0]

	t_CODE = r'[cvCVBEsn]'

	def t_NUMBER(t):
			r'\d+'
			t.value = int(t.value)
			return t

	def t_error(t):
		print "Illegal character '%s'" % t.value[0]

	return lex.lex()


def name_parser():
	import ply.yacc as yacc

	def p_primitive_code(p):
		'''primitive : CODE'''
		p[0] = ('CODE', p[1])

	def p_primitive_literal(p):
		'''primitive : TEXT'''
		p[0] = ('LITERAL', p[1])

	def p_primitive_var(p):
		'''primitive : '&' IDENTIFIER'''
		p[0] = ('VAR', p[2])

	def p_percent(p):
		'''percent : NUMBER '%' '''
		p[0] = ('PERCENT', p[1])

	def p_part(p):
		'''part : primitive
		        | group'''
		p[0] = p[1]

	def p_part_optional(p):
		'''part : primitive '?'
		        | group '?'
		'''
		p[0] = ('OPTIONAL', p[1], None)

	def p_part_optional_percent(p):
		'''part : primitive '?' percent
		        | group '?' percent
		'''
		p[0] = ('OPTIONAL', p[1], p[3])

	def p_sequence_empty(p):
		'''sequence :'''
		p[0] = ('SEQUENCE',[])

	def p_sequence_part(p):
		'''sequence : part'''
		p[0] = p[1]

	def p_sequence_parts(p):
		'''sequence : part part'''
		p[0] = ('SEQUENCE', [p[1], p[2]])

	def p_sequence_sequence(p):
		'''sequence : sequence part'''
		p[0] = ('SEQUENCE', p[1][1] + [p[2]])

	def p_group(p):
		'''group : '(' sequence ')'
		         | '(' choice ')'
		'''
		#p[0] = ('GROUP', p[2])
		p[0] = p[2]

	def p_choice(p):
		'''choice : sequence '|' sequence'''
		p[0] = ('CHOICE', [('OPTION',p[1],None), ('OPTION',p[3],None)])

	def p_choice_percent(p):
		'''choice : sequence '|' percent sequence'''
		p[0] = ('CHOICE', [('OPTION',p[1], p[3]), ('OPTION', p[4],None)])

	def p_choices_seq(p):
		'''choice : sequence '|' choice'''
		p[0] = ('CHOICE', [('OPTION',p[1],None)] + p[3][1])

	def p_choices(p):
		'''choice : sequence '|' percent choice'''
		p[0] = ('CHOICE', [('OPTION',p[1],p[3])] +p[4][1])

	def p_part_set(p):
		'''part : primitive IDENTIFIER
		        | group IDENTIFIER
		'''
		p[0] = ('SET', p[2], p[1])

	def p_root(p):
		'''root : sequence
		        | choice
		'''
		p[0] = p[1]

	def p_error(p):
		print "Syntax error in input!"

	start = 'root'

	return yacc.yacc()

def make_string(data):
	if data == None:
		return 'nil'
	elif isinstance(data, tuple):
		string = '('
		for n in data:
			string += make_string(n) + ' '
		return string[:-1] + ')'
	elif isinstance(data, str):
		return data
	elif isinstance(data, list):
		string = '(list'
		for n in data:
			string += ' ' + make_string(n)
		return string + ')'
	elif isinstance(data, int):
		return str(data)

if __name__ == '__main__':
	import pprint
	pp = pprint.PrettyPrinter(indent=3)
	parser = name_parser()
	thing = parser.parse('((B|c)(v|V)|c?v)((EB|B)v|E(v|||)|s(v|||))', lexer=name_lexer())
	#pp.pprint(parser.parse("((c[y](v||)(c|v?)|{art})v&[x]s|12%E|c|CV?nB)[e]", lexer=name_lexer()))
	#pp.pprint(parser.parse('((B|c)(v|V)|c?v)((EB|B)v|E(v|||)|s(v|||))', lexer=name_lexer()))
	print make_string(thing)
	#while 1:
		#try:
			#s = raw_input('pattern > ')
		#except EOFError:
			#break
		#pp.pprint(parser.parse(s))
