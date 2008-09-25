from django.shortcuts import render_to_response

from dividedposterity.models import Hero, Buff, Effect, PVMCombat

def route(request):
	"""Should support performing most actions in order to avoid redirects."""
	#hero = Hero.get_by_id(3)
	hero = Hero.all().get()
	
	context = {}
	if hero!=None:
		context = hero._display()
		context['wellbeing']={
			"hp":(hero.hp - hero.combat.player_hp_lost),
			"mp":(hero.mp - hero.combat.player_mp_used),
			"percenthp":(100*(hero.hp - hero.combat.player_hp_lost) / hero.hp),
			"percentmp":(100*(hero.mp - hero.combat.player_mp_used) / hero.mp)
		} if hero.combat!=None else {}

	return render_to_response("combat.djt",context)
