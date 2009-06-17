# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response

from models import CombatMessage, Enemy

import random, json

def index(request):
	return render_to_response('main/index.djt',{})

def startcombat(request):
	enemy = random.choice(Enemy.objects.all())
	combat = {}
	combat['enemy'] = enemy
	combat['turn'] = 0
	combat['done'] = False
	request.session['combat'] = combat
	return HttpResponseRedirect('/combat')

def combat(request):
	combat = request.session['combat']
	combat['turn'] += 1
	combat_text = []

	combat_status = CombatMessage.objects.filter(action='who')
	who_message = random.choice(combat_status)
	combat_text.append(who_message.transmogrify(combat['enemy']))

	if 'hit' in request.POST:
		#do hit stuff
		you_messages = CombatMessage.objects.filter(action='you hit')
		you_message = random.choice(you_messages)
		you_message = you_message.transmogrify(combat['enemy'])
		combat_text.append(you_message)
	elif 'miss' in request.POST:
		#do miss stuff
		you_messages = CombatMessage.objects.filter(action='you miss')
		you_message = random.choice(you_messages)
		you_message = you_message.transmogrify(combat['enemy'])
		combat_text.append(you_message)
	if 'win' in request.POST:
		#do win stuff
		combat['result'] = 'won'
		combat['done'] = True
	elif 'lose' in request.POST:
		#do lose stuff
		combat['result'] = 'lost'
		combat['done'] = True

	request.session['combat'] = combat
	if combat['done']:
		return HttpResponseRedirect('/aftercombat')


	enemy_miss = CombatMessage.objects.filter(action='enemy misses')
	enemy_message = random.choice(enemy_miss)
	combat_text.append(enemy_message.transmogrify(combat['enemy']))

	t = loader.get_template('main/combat.djt')
	c = Context({
			'combat_text': combat_text,
			'turn': combat['turn']
		})
	return HttpResponse(t.render(c))

def aftercombat(request):
	return render_to_response('main/aftercombat.djt', request.session['combat'])
