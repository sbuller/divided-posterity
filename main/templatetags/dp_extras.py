# -*- coding: utf-8 -*-

from main.models import Location
from django import template
from django.utils.safestring import SafeUnicode

register = template.Library()

@register.filter(name="get_map_data")
def get_map_data(var, args):
	for it in var:
		if it.slug == args:
			return SafeUnicode("<a href=\"/travel/" + it.slug + "\">" + it.name + "</a>")
	return "empty"