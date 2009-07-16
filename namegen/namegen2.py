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

def evaluate(node, dictionary):
	import random
	def do_set():
		val = evaluate(node[2], dictionary)
		dictionary[node[1]] = val
		return val
	def do_option():
		return evaluate(node[1], dictionary)
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
		num = random.randint(1,100)
		if num>total:
			return evaluate(random.choice(options_residue), dictionary)
		for option in options_explicit:
			if option[1] <= num:
				return evaluate(option[0], dictionary)
		return "NO OPTION"
	def do_sequence():
		result = ""
		for n in node[1]:
			result += evaluate(n, dictionary)
		return result
	def do_optional():
		val = evaluate(node[1], dictionary)
		if node[2] == None:
			percent = 50
		else:
			percent = evaluate(node[2],dictionary)
		if random.randint(1,100)<=percent:
			return val
		return ''
	def do_percent():
		return node[1]
	def do_var():
		return dictionary[node[1]]
	def do_code():
		return random.choice(DEFAULT_PRIMITIVES[node[1]])

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

if __name__ == '__main__':
	import sys, os, math
	if 2==len(sys.argv):
		names = map(lambda x:evaluate(tree,{}),xrange(int(sys.argv[1])))
	else:
		print evaluate(tree, {})
		sys.exit(0)

	if sys.stdout.isatty():
		def max_len(array):
			return max(map(len,array))

		height, width = map(int,os.popen('stty size', 'r').read().split())
		min_cols = width/(max_len(names)+1)
		max_cols = min([int(width/5),len(names)])
		awesome = []
		for i in xrange(min_cols,max_cols+1):
			inx = range(0,len(names),int(math.ceil(len(names)/float(i))))
			col_width = []
			for it in inx:
				col_width.append(max_len(names[it:it+int(math.ceil(len(names)/float(i)))])+1)
			if sum(col_width) <= width:
				awesome.append(col_width)
			else:
				awesome.append(False)
		cw = filter(None,awesome).pop()
		num_cols = len(cw)
		num_rows = int(math.ceil(len(names)/float(num_cols)))
		for row in xrange(num_rows):
			for col in xrange(num_cols):
				i = row + col*num_rows
				if i < len(names):
					print names[i].ljust(cw[col]-1),
			print
	else:
		print '\n'.join(names)
