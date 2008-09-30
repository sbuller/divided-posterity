from django import template
from django.template.defaulttags import URLNode

register = template.Library()

def dpurl(parser, token):
	bits = token.contents.split(' ')
	if len(bits) < 2:
		raise TemplateSyntaxError("'%s' takes at least one argument"
		                          " (path t    o a view)" % bits[0])
	viewname = bits[1]
	args = []
	kwargs = {}
	asvar = None
	
	if len(bits) > 2:
		bits = iter(bits[2:])
		for bit in bits:
			if bit == 'as':
				asvar = bits.next()
				break
			else:
				for arg in bit.split(","):
					if '=' in arg:
						k, v = arg.split('=', 1)
						k = k.strip()
						kwargs[k] = parser.compile_filter(v)
					elif arg:
						args.append(parser.compile_filter(arg))
	return URLNode("dividedposterity.controllers.%s.route" % viewname, args, kwargs, asvar)

dpurl = register.tag(dpurl)
