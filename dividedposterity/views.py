from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.ext import db

from dividedposterity.models import Hero, Buff, Effect, PVMCombat
# Create your views here.

def statstuff(hero,stat):
	if hero == None:
		return {'stat':stat, 'base':'-', 'value':'-', 'change':'-'}
	base = getattr(hero, "base%s" % stat.lower())
	value = getattr(hero, stat.lower())
	#change = (changed>base)?"increased":(changed<base)?"decreased":"uncreased"
	change = "increased" if value>base else "decreased" if value<base else "uncreased"
	return {'stat':stat, 'base':base, 'value':value, 'change':change}

def index(request, template):
	"""This stuff provides the information for layout.djt. It needs to be
	offered as a helper or something for other functions.
	"""
	t = loader.get_template("%s.djt" % template)
	#hero = Hero.get_by_id(3)
	hero = Hero.all().get()
	buffs = Buff.all().filter('target = ', hero).order('sourcename').order('buffname').fetch(100)
	effects = Effect.all().filter('target = ', hero).order('order').order('quantity').fetch(100)
	return HttpResponse (t.render(Context({
	                     'hero':hero,
	                     'buffs':buffs,
	                     'effects':effects,
	                     'stats':[ statstuff(hero,"Brawn"),
	                               statstuff(hero,"Magery"),
	                               statstuff(hero,"Stamina"),
	                               statstuff(hero,"Finesse"),
	                               statstuff(hero,"Charm"),
	                               statstuff(hero,"Lore")]
	                     })))

def create(request, model):
	"""This needs to be eliminated in favour of an automatic controller/template
	thingy for introspecting a model, and yielding relevent code.
	"""
	{
		'hero': lambda r: Hero(
			name=r.POST['name'],
			ID=int(r.POST['id']),
			cclass=r.POST['cclass'],

			brawn=int(r.POST['brawn']),
			magery=int(r.POST['magery']),
			stamina=int(r.POST['stamina']),
			finesse=int(r.POST['finesse']),
			charm=int(r.POST['charm']),
			lore=int(r.POST['lore']),

			basebrawn=int(r.POST['basebrawn']),
			basemagery=int(r.POST['basemagery']),
			basestamina=int(r.POST['basestamina']),
			basefinesse=int(r.POST['basefinesse']),
			basecharm=int(r.POST['basecharm']),
			baselore=int(r.POST['baselore']),

			hp=int(r.POST['hp']),
			mp=int(r.POST['mp'])
			),
		'buff': lambda r: Buff(
			target=Hero.get_by_id(int(request.POST['target'])),
			source=Hero.get_by_id(int(request.POST['source'])),
			sourcename=request.POST['sourcename'],
			buffname=request.POST['buffname']
			),
		'effect': lambda r: Effect(
			effectname=request.POST['effectname'],
			target=Hero.get_by_id(int(request.POST['target'])),
			quantity=int(request.POST['quantity']),
			unit=request.POST['unit'],
			order=1
			)
	}[model](request).save()
	return HttpResponseRedirect('/inventory')

def combat(request):
	"""Should support performing most actions in order to avoid redirects."""
	t = loader.get_template("combat.djt")
	#hero = Hero.get_by_id(3)
	hero = Hero.all().get()
	buffs = Buff.all().filter('target = ', hero).order('sourcename').order('buffname').fetch(100)
	effects = Effect.all().filter('target = ', hero).order('order').order('quantity').fetch(100)
	#wellbeing = {'hp': hero.hp - hero.combat.player_hp_lost,
	#             'mp': hero.mp - hero.combat.player_mp_used,
	#             'percenthp': (hero.hp - hero.combat.player_hp_lost) / hero.hp,
	#             'percentmp': (hero.mp - hero.combat.player_mp_used) / hero.mp
	#            }
	return HttpResponse (t.render(Context({
	                     'hero':hero,
	                     'buffs':buffs,
	                     'effects':effects,
	                     'stats':[ statstuff(hero,"Brawn"),
	                               statstuff(hero,"Magery"),
	                               statstuff(hero,"Stamina"),
	                               statstuff(hero,"Finesse"),
	                               statstuff(hero,"Charm"),
	                               statstuff(hero,"Lore")],
	                     'wellbeing':{"hp":(hero.hp - hero.combat.player_hp_lost),
	                                  "mp":(hero.mp - hero.combat.player_mp_used),
	                                  "percenthp":(100*(hero.hp - hero.combat.player_hp_lost) / hero.hp),
	                                  "percentmp":(100*(hero.mp - hero.combat.player_mp_used) / hero.mp)
	                                 }
	                     })))
def startcombat(request):
	hero = Hero.all().get()
	combat = PVMCombat(player_hp_lost=0, player_mp_used=0, monster_hp_lost=0,
                     monster_mp_used=0, effects=[], behaviour_data="", turn=0)
	combat.put()
	hero.combat = combat
	hero.put()
	return HttpResponseRedirect('/combat')

def defaultredirect(request):
	return HttpResponseRedirect('/combat')