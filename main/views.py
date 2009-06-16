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
	request.session['enemy'] = enemy
	return HttpResponseRedirect('/combat/')

def combat(request):
	t = loader.get_template('main/combat.djt')
	enemy = request.session['enemy']
	combat_status = CombatMessage.objects.filter(action='who')
	hit = CombatMessage.objects.filter(action='you hit')
	enemy_miss = CombatMessage.objects.filter(action='enemy misses')
	whomessage = random.choice(combat_status)
	youmessage = random.choice(hit)
	enemymessage = random.choice(enemy_miss)
	c = Context({
			'combat_text': [
			whomessage.transmogrify(enemy),
			youmessage.transmogrify(enemy),
			enemymessage.transmogrify(enemy)]
		})
	return HttpResponse(t.render(c))
