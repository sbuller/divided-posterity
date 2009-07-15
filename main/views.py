# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader, RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from models import Message, Enemy, Item, Location, Combat, InventoryItem, Hero, EncounterInfo

import random, json

def not_during_combat(fn):
	def wrap(*args, **kwargs):
		hero = Hero.objects.filter(user=args[0].user)[0]
		if (hero.combat and not hero.combat.done):
			return HttpResponseRedirect('/combat')
		return fn(*args,**kwargs)
	return wrap

def index(request):
	if request.user.is_authenticated():
		hero = Hero.objects.filter(user=request.user)[0]
		return render_to_response('main.djt', {}, RequestContext(request))
	else:
		return render_to_response('index.djt')

@login_required
@not_during_combat
def startcombat(request, enemy=None):
	hero = Hero.objects.get(user=request.user)
	if not enemy:
		enemy = random.choice(Enemy.objects.all())
	combat = hero.new_pvm_combat(enemy)
	return render_to_response('combat.djt',{'combat':combat}, RequestContext(request))

@login_required
def combat(request):
	hero = Hero.objects.filter(user=request.user)[0]
	combat = hero.combat
	combat.next_round()

	if 'skill' in request.GET:
		skill = hero.skills.filter(pk=request.GET['skill'])
		if len(skill):
			skill[0].invoke(actor=hero, target=combat.enemies()[0], skill=skill[0])

	for en in combat.enemies():
		en.enemy.perform_action(en, combat)

	if 'win' in request.POST:
		combat.win()
	elif 'lose' in request.POST:
		combat.lose()

	combat.save()

	if combat.done:
		return HttpResponseRedirect('/aftercombat')

	return render_to_response('combat.djt', {'combat': combat}, RequestContext(request))

@login_required
@not_during_combat
def aftercombat(request):
	hero = Hero.objects.filter(user=request.user)[0]
	return render_to_response('aftercombat.djt', {'hero': hero}, RequestContext(request))

@login_required
def inventory(request):
	owner = Hero.objects.get(user=request.user)
	inventory = InventoryItem.objects.filter(owner=owner)
	return render_to_response('inventory.djt', {'items':inventory}, RequestContext(request))

@login_required
@not_during_combat
def locationMap(request):
	hero = Hero.objects.filter(user=request.user)[0]
	return render_to_response("maps/"+hero.location.slug+".djt", {'location':hero.location,'places':hero.location.neighbors.all()}, RequestContext(request))

@login_required
@not_during_combat
def travel(request, location_id):
	hero = Hero.objects.filter(user=request.user)[0]
	destination = Location.objects.get(slug=location_id)

	if (not destination in hero.location.neighbors.all() and destination != hero.location):
		return HttpResponse("What are you doing!?")
	hero.destination = destination
	hero.save()

	encounter_infos = EncounterInfo.objects.filter(location=hero.destination)

	total=0
	for it in encounter_infos:
		total = total + it.encounter_rate
	num = random.randint(1,total)

	for it in encounter_infos:
		if num >= 0:
			num = num - it.encounter_rate
			encounter_info = it

	if not encounter_info:
		return HttpResponse("Error. No random encounter generated.")

	if encounter_info.is_combat:
		return startcombat(request,encounter_info.enemy)
	else:
		return HttpResponse(encounter_info.encounter)

@login_required
@not_during_combat
def flush_inventory(request):
	if 'flush' in request.POST:
		hero = Hero.objects.filter(user=request.user)[0]
		print hero
		items = InventoryItem.objects.filter(owner=hero)
		print items
		items.delete()
	return HttpResponseRedirect('/inventory')
