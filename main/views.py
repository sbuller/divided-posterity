# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response

from models import CombatMessage, Enemy, Item, Location, Combat

import random, json

def index(request):
	return render_to_response('main/index.djt')

def startcombat(request):
	if not 'location' in request.session:
		request.session['location'] = random.choice(Location.objects.all())

	combat = Combat()
	request.session['combat'] = combat

	return render_to_response('main/combat.djt',{'turn':combat.turn})

def combat(request):
	combat = request.session['combat']
	combat.turn += 1
	combat_text = []

	location = request.session['location']

	messages = CombatMessage.objects

	combat_status = messages.filter(action='who')
	who_message = random.choice(combat_status)
	combat_text.append(who_message.transmogrify(combat.enemy, location))

	if 'youhit' in request.POST:
		if request.POST['youhit'] == 'true':
			you_messages = messages.filter(action='you hit')
		else:
			you_messages = messages.filter(action='you miss')
		you_message = random.choice(you_messages)
		you_message = you_message.transmogrify(combat.enemy, location)
		combat_text.append(you_message)

	if 'theyhit' in request.POST:
		if request.POST['theyhit'] == 'true':
			enemy_messages = messages.filter(action='enemy hits')
		else:
			enemy_messages = messages.filter(action='enemy misses')
		enemy_message = random.choice(enemy_messages)
		enemy_message = enemy_message.transmogrify(combat.enemy, location)
		combat_text.append(enemy_message)

	if 'win' in request.POST:
		combat.win()
	elif 'lose' in request.POST:
		combat.lose()

	request.session['combat'] = combat
	if combat.done:
		return HttpResponseRedirect('/aftercombat')

	return render_to_response('main/combat.djt', {
			'combat_text': combat_text,
			'turn': combat.turn
		})

def aftercombat(request):
	combat = request.session['combat']
	inventory = {}
	winitems = {}
	if 'inventory' in request.session:
		inventory = request.session['inventory']
	if combat.result == 'won':
		winitems[random.choice(Item.objects.all()).id] = 1
		while random.choice([True,False]):
			item = random.choice(Item.objects.all())
			if not item.id in winitems:
				winitems[item.id] = 1
			else:
				winitems[item.id] += 1
	outputitems = []
	keymap = Item.objects.in_bulk(winitems.keys())
	for key,value in winitems.iteritems():
		outputitems.append({'count':value, 'name':keymap[key].name})
		if key in inventory:
			inventory[key] += value
		else:
			inventory[key] = value
	request.session['inventory'] = inventory
	return render_to_response('main/aftercombat.djt', {'combat': request.session['combat'], 'items': outputitems})

def inventory(request):
	inventory = {}
	outputitems = []
	if 'inventory' in request.session:
		inventory = request.session['inventory']
	keymap = Item.objects.in_bulk(inventory.keys())
	for itemid, count in inventory.iteritems():
		outputitems.append({'count':count, 'name':keymap[itemid].name})
	return render_to_response('main/inventory.djt', {'items':outputitems})

def locationMap(request, location_id=1):
	location = Location.objects.get(id=location_id)
	children = Location.objects.filter(parent=location)
	siblings = Location.objects.filter(parent=location.parent).exclude(id=location_id)
	request.session['location'] = location
	return render_to_response('main/map.djt', {'location':location,'children':children,'siblings':siblings})
