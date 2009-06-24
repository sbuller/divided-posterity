# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from models import CombatMessage, Enemy, Item, Location, Combat, InventoryItem, Hero

import random, json

def index(request):
	if request.user.is_authenticated():
		return render_to_response('main/main.djt')
	else:
		return render_to_response('main/index.djt')

@login_required
def startcombat(request):
	if not 'location' in request.session:
		request.session['location'] = random.choice(Location.objects.all())

	combat = Combat(request.session['location'])
	request.session['combat'] = combat

	return render_to_response('main/combat.djt',{'combat':combat})

@login_required
def combat(request):
	combat = request.session['combat']
	combat.next_round()

	if 'youhit' in request.POST:
		if request.POST['youhit'] == 'true':
			combat.youhit()
		else:
			combat.youmiss()
	if 'theyhit' in request.POST:
		if request.POST['theyhit'] == 'true':
			combat.theyhit()
		else:
			combat.theymiss()

	if 'win' in request.POST:
		combat.win()
	elif 'lose' in request.POST:
		combat.lose()

	request.session['combat'] = combat
	if combat.done:
		return HttpResponseRedirect('/aftercombat')

	return render_to_response('main/combat.djt', {'combat': combat})

@login_required
def aftercombat(request):
	combat = request.session['combat']
	winitems = {}
	if combat.won():
		winitems[random.choice(Item.objects.all()).id] = 1
		while random.choice([True,False]):
			item = random.choice(Item.objects.all())
			if not item.id in winitems:
				winitems[item.id] = 1
			else:
				winitems[item.id] += 1
	outputitems = []
	keymap = Item.objects.in_bulk(winitems.keys())
	owner = Hero.objects.get(user=request.user)
	for key,value in winitems.iteritems():
		outputitems.append({'count':value, 'name':keymap[key].name})
		InventoryItem.add_item(owner,keymap[key],value)
	return render_to_response('main/aftercombat.djt', {'combat': request.session['combat'], 'items': outputitems})

@login_required
def inventory(request):
	owner = Hero.objects.get(user=request.user)
	inventory = InventoryItem.objects.filter(owner=owner)
	return render_to_response('main/inventory.djt', {'items':inventory})

@login_required
def locationMap(request, location_id=1):
	location = Location.objects.get(id=location_id)
	children = Location.objects.filter(parent=location)
	siblings = Location.objects.filter(parent=location.parent).exclude(id=location_id)
	request.session['location'] = location
	return render_to_response('main/map.djt', {'location':location,'children':children,'siblings':siblings})
