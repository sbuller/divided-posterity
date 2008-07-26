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

def createHero(request):
	return Hero(
			name=request.POST['name'],
			ID=int(request.POST['id']),
			cclass=request.POST['cclass'],

			brawn=int(request.POST['brawn']),
			magery=int(request.POST['magery']),
			stamina=int(request.POST['stamina']),
			finesse=int(request.POST['finesse']),
			charm=int(request.POST['charm']),
			lore=int(request.POST['lore']),

			basebrawn=int(request.POST['basebrawn']),
			basemagery=int(request.POST['basemagery']),
			basestamina=int(request.POST['basestamina']),
			basefinesse=int(request.POST['basefinesse']),
			basecharm=int(request.POST['basecharm']),
			baselore=int(request.POST['baselore'])
			)

def createBuff(request):
	return Buff(
			target=Hero.get_by_id(int(request.POST['target'])),
			source=Hero.get_by_id(int(request.POST['source'])),
			sourcename=request.POST['sourcename'],
			buffname=request.POST['buffname']
			)

def createEffect(request):
	return Effect(
			effectname=request.POST['effectname'],
			target=Hero.get_by_id(int(request.POST['target'])),
			quantity=int(request.POST['quantity']),
			unit=request.POST['unit'],
			order=1
			)

def create(request, model):
	{'hero': createHero,
	 'buff': createBuff,
	 'effect': createEffect
	}[model](request).save()
	return HttpResponseRedirect('/inventory.html')
