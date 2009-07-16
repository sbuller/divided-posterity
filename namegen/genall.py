# -*- coding: utf-8 -*-

DEFAULT_PRIMITIVES = { #t=template, v=vowel, vg=vowel group, c=consonant, cgb=beginning-of-word consonant group, cge=end-of-word consonant group, s=syllable, n=name
	't':'((B|c)(v|V)|c?v)((EB|B)v|E(v|||)|s(v|||))',
	'v':'a,e,i,o,u,y',
	'V':'ae,ai,au,ea,ew,ia,oe',
	'c':'b,c,d,f,g,h,j,k,l,m,n,p,qu,r,s,t,v,w,x,y,z',
	'B':'bl,br,bw,ch,cl,cr,cw,dr,dw,fl,fr,gh,gl,gn,gr,gw,kh,kl,kn,kr,kw,ph,pl,pr,ps,rh,sc,sch,scr,sh,shr,sk,skr,sl,sm,sn,sp,spl,spr,st,str,sw,th,tr,tw,wh,wr,zh',
	'E':'ch,ck,ct,ff,ft,gh,ght,lch,ld,ll,lm,lp,lsk,lt,lth,mb,mn,mp,nch,nd,ng,ngth,nk,nt,nth,nst,nx,nz,ph,pt,rb,rch,rd,rg,rk,rl,rlst,rlt,rlth,rm,rn,rnt,rnth,rsh,rsp,rst,rt,rth,sh,sk,st,th',
	's':'ash,brom,chum,dan,dar,dock,faze,gamm,gler,grim,han,ine,ish,jar,jem,lash,lim,lom,nock,ock,ore,phiz,plad,prem,quin,quol,rath,sham,shrie,thar,thow,ton,ulf,wan,whel,yen,yul,zhul',
	'n':'steve,dave,eldon'
}
DEFAULT_PRIMITIVES['C'] = DEFAULT_PRIMITIVES['B']+DEFAULT_PRIMITIVES['E']
for s in DEFAULT_PRIMITIVES:
	DEFAULT_PRIMITIVES[s] = DEFAULT_PRIMITIVES[s].split(',')

import nameparse

parser = nameparse.name_parser()
lexer = nameparse.name_lexer()

tree = parser.parse(DEFAULT_PRIMITIVES['t'][0], lexer=lexer)

class bang(object):
	""" a generator with saved state that can be reset """
	def __init__(self, arg):
		self.arg = arg
		self.reset()
	def __iter__(self):
		for item in self.iterable:
			yield item
	def next(self):
		return self.iterable.next()
	def reset(self):
		if hasattr(self.arg, '__iter__') and \
				hasattr(self.arg, 'next') :
			self.iterable = self.arg
		elif hasattr(self.arg, '__getitem__'):
			if self.arg:
				self.iterable = iter(self.arg)
			else: self.iterable = iter([""])
		else:
			self.iterable = iter([self.arg])
	def __repr__(self):
		return repr(self.arg)

def concatenate(g1, g2):
	"""Lazy evaluation concatenation """
	#list, tuple, and string iterators are not used implicitly
	#Not generalized for sequences other than strings
	if hasattr(g1, '__iter__') and hasattr(g2, '__iter__'):
		#concatenations of left items to right items
		#map(operator.plus, leftseq, rightseq)
		gt = list(g2)
		for x in g1:
			for y in gt:
				yield x + y
	elif hasattr(g1, '__iter__') :
		#concatenations of left items to right sequence
		#map(operator.plus, [leftseq]*len(rightseq), rightseq)
		for x in g1:
			yield x + g2
	elif hasattr(g2, '__iter__') :
		#concatenations of left sequence to right items
		#map(operator.plus, leftseq, [rightseq]*len(leftseq))
		for x in g2:
			yield g1 + x
	else:
		#string concatenation like Python
		yield g1 + g2

def evaluate(node, dictionary):
	def do_set():
		for val in evaluate(node[2], dictionary):
			dictionary[node[1]] = val
			yield val
	def do_option():
		for n in evaluate(node[1], dictionary):
			yield n
	def do_choice():
		options_explicit = []
		options_residue = []
		total = 0
		for n in node[1]:
			percent = n[2]
			if percent == None:
				options_residue.append(n)
			else:
				total += percent[1]
				options_explicit.append((n,total))
		for option in options_residue:
			for n in evaluate(option, dictionary):
				yield n
		for option in options_explicit:
			for n in evaluate(option[0], dictionary):
				yield n
	def do_sequence():
		from itertools import repeat
		results = repeat('',1)
		for n in node[1]:
			results = concatenate(results, evaluate(n, dictionary))
		for result in results:
			yield result
	def do_optional():
		yield ''
		for n in evaluate(node[1], dictionary):
			yield n
	def do_percent():
		return node[1]
	def do_var():
		yield dictionary[node[1]]
	def do_code():
		for n in DEFAULT_PRIMITIVES[node[1]]:
			yield n

	functions = {
		'SET': do_set,
		'OPTION': do_option,
		'CHOICE': do_choice,
		'SEQUENCE': do_sequence,
		'OPTIONAL': do_optional,
		'PERCENT': do_percent,
		'VAR': do_var,
		'LITERAL': lambda: node[1],
		'CODE': do_code,
	}
	return functions[node[0]]()

for n in evaluate(tree, {}):
	print n
