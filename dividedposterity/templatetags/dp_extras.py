from django import template
from django.template.defaulttags import URLNode

register = template.Library()

def dpurl(parser, token):
	bits = token.contents.split(' ', 2)
	if len(bits) < 2:
		raise TemplateSyntaxError, "'%s' takes at least one argument (path t    o a view)" % bits[0]
	args = []
	kwargs = {}
	if len(bits) > 2:
		for arg in bits[2].split(','):
			if '=' in arg:
				k, v = arg.split('=', 1)
				kwargs[k] = parser.compile_filter(v)
			else:
				args.append(parser.compile_filter(arg))
	return URLNode("dividedposterity.controllers.%s.route" % bits[1], args, kwargs)

dpurl = register.tag(dpurl)
