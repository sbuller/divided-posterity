from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.ext import db

from dividedposterity.models import Hero, Buff, Effect
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
			baselore=int(r.POST['baselore'])
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
