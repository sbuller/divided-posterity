from django.shortcuts import render_to_response

from dividedposterity.models import Hero, Buff, Effect

def route(request, template):
	#hero = Hero.get_by_id(3)
	hero = Hero.all().get()
	return render_to_response("%s.djt" % template,hero._display() if hero!=None else {})