# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader, RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from models import Message, Enemy, Item, Location, Combat, InventoryItem, Hero

import random, json

def index(request):
	if request.user.is_authenticated():
		hero = Hero.objects.get(user=request.user)
		return render_to_response('main/main.djt', {}, RequestContext(request))
	else:
		return render_to_response('main/index.djt')

@login_required
def startcombat(request):
	hero = Hero.objects.get(user=request.user)
	combat = hero.new_pvm_combat(random.choice(Enemy.objects.all()))
	return render_to_response('gen1/combat.djt',{'combat':combat}, RequestContext(request))

@login_required
def combat(request):
	hero = Hero.objects.filter(user=request.user)[0]
	combat = hero.combat
	combat.next_round()

	if 'youhit' in request.POST:
		if request.POST['youhit'] == 'true':
			combat.challenger_hit()
		else:
			combat.challenger_miss()
	if 'theyhit' in request.POST:
		if request.POST['theyhit'] == 'true':
			combat.opposition_hit()
		else:
			combat.opposition_miss()

	if 'win' in request.POST:
		combat.win()
	elif 'lose' in request.POST:
		combat.lose()


	combat.save()

	if combat.done:
		return HttpResponseRedirect('/aftercombat')

	return render_to_response('gen1/combat.djt', {'combat': combat}, RequestContext(request))

@login_required
def aftercombat(request):
	hero = Hero.objects.filter(user=request.user)[0]
	combat = hero.combat
	if combat.challenger.enemy:
		challenger = combat.challenger
		combat.challenger = None
		combat.save()
		challenger.delete()
	if combat.opposition.enemy:
		opposition = combat.opposition
		combat.opposition = None
		combat.save()
		opposition.delete()
	return render_to_response('main/aftercombat.djt', {'combat': combat}, RequestContext(request))

@login_required
def inventory(request):
	owner = Hero.objects.get(user=request.user)
	inventory = InventoryItem.objects.filter(owner=owner)
	return render_to_response('gen1/inventory.djt', {'items':inventory}, RequestContext(request))

@login_required
def locationMap(request):
	hero = Hero.objects.filter(user=request.user)[0]
	return render_to_response("main/maps/"+hero.location.slug+".djt", {'location':hero.location,'places':hero.location.neighbors.all()}, RequestContext(request))

@login_required
def travel(request, location_id):
	hero = Hero.objects.filter(user=request.user)[0]
	new_location = Location.objects.get(slug=location_id)

	if (not new_location in hero.location.neighbors.all() and new_location != hero.location):
		return HttpResponse("What are you doing!?")
	hero.location = new_location
	hero.save()

	return startcombat(request)
