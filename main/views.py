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
	request.session['combat'] = combat
	return HttpResponseRedirect('/combat')

def combat(request):
	t = loader.get_template('main/combat.djt')
	combat = request.session['combat']
	combat['turn'] += 1

	combat_status = CombatMessage.objects.filter(action='who')
	hit = CombatMessage.objects.filter(action='you hit')
	enemy_miss = CombatMessage.objects.filter(action='enemy misses')

	whomessage = random.choice(combat_status)
	youmessage = random.choice(hit)
	enemymessage = random.choice(enemy_miss)

	request.session['combat'] = combat
	c = Context({
			'combat_text': [
			whomessage.transmogrify(combat['enemy']),
			youmessage.transmogrify(combat['enemy']),
			enemymessage.transmogrify(combat['enemy'])],
			'turn': combat['turn']
		})
	return HttpResponse(t.render(c))
