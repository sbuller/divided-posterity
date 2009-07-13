#!/usr/bin/python
# -*- coding: utf-8 -*-

#template syntax:
	#c=consonant,
	#v=vowel,
	#C=consonant group,
	#V=vowel group,
	#B=consonant group suitable for beginning of name
	#E=consonant group suitable for end of name
	#s=syllable
	#n=name
	#modifiers:
		#?=Once or no times
		#|='or'
		#()=grouping
	#planned stuff:
		#?num%=once or no times (num = chance to include)
		#|num%=likelihood (used with 'or's)
		#[num] = save random choice to var[num]
	#&[num]=recall var[num]
	#{}=treat everything in here as literal

import random

DEFAULT_PRIMITIVES = { #t=template, v=vowel, vg=vowel group, c=consonant, cgb=beginning-of-word consonant group, cge=end-of-word consonant group, s=syllable, n=name
	't':'((B|c)(v|V)|c?v)((EB|B)v|E(v|||)|s(v|||))',
	'v':'a,e,i,o,u,y',
	'vg':'ae,ai,au,ea,ew,ia,oe',
	'c':'b,c,d,f,g,h,j,k,l,m,n,p,qu,r,s,t,v,w,x,y,z',
	'cgb':'bl,br,bw,ch,cl,cr,cw,dr,dw,fl,fr,gh,gl,gn,gr,gw,kh,kl,kn,kr,kw,ph,pl,pr,ps,rh,sc,sch,scr,sh,shr,sk,skr,sl,sm,sn,sp,spl,spr,st,str,sw,th,tr,tw,wh,wr,zh',
	'cge':'ch,ck,ct,ff,ft,gh,ght,ld,ll,lm,lp,lt,mb,mn,mp,nd,ng,nk,nt,nst,nx,nz,ph,pt,rb,rch,rd,rg,rk,rl,rlst,rlt,rlth,rm,rn,rnt,rsh,rsp,rst,rt,rth,sh,sk,st,th',
	's':'ash,brom,chum,dan,dar,dock,faze,gamm,gler,grim,han,ine,ish,jar,jem,lash,lim,lom,nock,ock,ore,phiz,plad,prem,quin,quol,rath,sham,shrie,thar,thow,ton,ulf,wan,whel,yen,yul,zhul',
	'n':'steve,dave,eldon'
}

class NameGen():
	def __init__(self, dic=DEFAULT_PRIMITIVES):
		self.templ = dic['t'].split(',')
		self.v = dic['v'].split(',')
		self.c = dic['c'].split(',')
		self.V = dic['vg'].split(',')
		self.B = dic['cgb'].split(',')
		self.E = dic['cge'].split(',')
		self.C = self.B + self.E
		self.s = dic['s'].split(',')
		self.n = dic['n'].split(',')

	def gen_names(self, num=1):
		def grab(ch):
			if ch in self.__dict__.keys():
				return random.choice (self.__dict__[ch])
			else:
				return '<Error:Invalid Template Key>'

		def parse(st, txt=''):
			if len(st) <= 0:
				return txt
			st0 = st[0]

			if st0 == '?':
				return random.choice([txt,'']) + parse(st[1:])
			elif st0 == '(':
				count = 1
				i = 1
				pipes = [0]
				while count > 0 and i < len(st):
					if st[i] == '(':
						count += 1
					elif st[i] == ')':
						count -= 1
					if (count == 0 and st[i] == ')') or (count == 1 and st[i] == '|'):
						pipes.append(i)
					i += 1
				if count > 0:
					return '<Error:Template Parentheses Mismatch>'
				else:
					i = 0
					c = []
					while i < len(pipes) - 1:
						c.append(st[pipes[i]+1:pipes[i+1]])
						i += 1
					#print st, pipes
				return txt + parse(random.choice(c)) + parse(st[pipes[len(pipes)-1]+1:])
			elif st0 in 'vcVCBEsn':
				return txt + parse(st[1:], grab(st0))
			elif st0 == ')':
				return '<Error:Template Parentheses Mismatch>'
			else:
				return '<Error:Template Key \"'+st0+'\" Not Recognized>'

		names = []
		while len(names) < num:
			names.append(parse('('+random.choice(self.templ)+')'))
		return names

	def gen_name(self):
		return self.gen_names(1)[0]

if __name__ == '__main__':
	import sys, os, math
	if 2==len(sys.argv):
		names = NameGen().gen_names(int(sys.argv[1]))
	else:
		print NameGen().gen_name()
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
