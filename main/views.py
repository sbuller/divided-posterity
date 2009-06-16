# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response

from models import CombatMessage, Enemy

import random, json

def index(request):
	return render_to_response('main/index.djt',{})

def combat(request):
	t = loader.get_template('main/combat.djt')
	enemy = Enemy.objects.filter(name='Billy-Joe').get()
	combat_status = CombatMessage.objects.filter(action='who')
	hit = CombatMessage.objects.filter(action='you hit')
	enemy_miss = CombatMessage.objects.filter(action='enemy misses')
	whomessage = random.choice(combat_status)
	youmessage = random.choice(hit)
	enemymessage = random.choice(enemy_miss)
	c = Context({
			'combat_text': [
			whomessage.message.format(en=enemy, words=map(lambda x: x[enemy.plurality], json.loads(whomessage.words))),
			youmessage.message.format(en=enemy,words=map(lambda x: x[enemy.plurality], json.loads(youmessage.words))),
			enemymessage.message.format(en=enemy,words=map(lambda x: x[enemy.plurality],json.loads(enemymessage.words))),]
		})
	return HttpResponse(t.render(c))
