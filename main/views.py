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

	if 'hit' in request.POST:
		#do hit stuff
		1
	elif 'miss' in request.POST:
		#do miss stuff
		1
	elif 'win' in request.POST:
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

	combat_status = CombatMessage.objects.filter(action='who')
	hit = CombatMessage.objects.filter(action='you hit')
	enemy_miss = CombatMessage.objects.filter(action='enemy misses')

	whomessage = random.choice(combat_status)
	youmessage = random.choice(hit)
	enemymessage = random.choice(enemy_miss)

	t = loader.get_template('main/combat.djt')
	c = Context({
			'combat_text': [
			whomessage.transmogrify(combat['enemy']),
			youmessage.transmogrify(combat['enemy']),
			enemymessage.transmogrify(combat['enemy'])],
			'turn': combat['turn']
		})
	return HttpResponse(t.render(c))

def aftercombat(request):
	return render_to_response('main/aftercombat.djt', request.session['combat'])
