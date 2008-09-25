from django.http import HttpResponseRedirect

from dividedposterity.models import Hero, PVMCombat

def route(request):
	hero = Hero.all().get()
	combat = PVMCombat(player_hp_lost=0, player_mp_used=0, monster_hp_lost=0,
                     monster_mp_used=0, effects=[], behaviour_data="", turn=0)
	combat.put()
	hero.combat = combat
	hero.put()
	return HttpResponseRedirect('/combat')
