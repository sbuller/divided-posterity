# -*- coding: utf-8 -*-

from main.models import Location
from django import template
from django.utils.safestring import SafeUnicode

register = template.Library()

@register.filter
def get_map_data(var, arg):
	for it in var:
		if it.slug == arg:
			return SafeUnicode("<a href=\"/travel/" + it.slug + "\">" + it.name + "</a>")
	return "empty"

@register.filter
def pronoun(var, arg):
	table = [ #m,f,n,p,y
		['him','her','it','them','you'], #em
		['he','she','it','they','you'], #ey
		['his','her','its','their','your'], #eir
		['his','hers','its','theirs','yours'], #eirs
		['himself','herself','itself','themselves','yourself'] #emself
	]
	gender = ['m','f','n']
	spivak = ['em','ey','eir','eirs','emself']
	col = var.player_pov*4 or (not (not var.count-1))*3 or gender.index(var.gender)
	return table[spivak.index(arg)][col]

@register.filter
def conj(var, arg):
	#Order of arguments: 3rd person singular, 3rd person plural, 2nd person
	args= arg.split(",")
	return args[var.player_pov*2 or not (not var.count-1)]

@register.filter
def percent(var, arg):
	return var.__getattribute__(arg) * 100.0 / var.__getattribute__("max_"+arg)
