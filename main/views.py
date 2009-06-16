# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
import random

ref_strings = {
	'combat_status': [
		["You are fighting {en[name]}, the {en[type]}",[]],
		["{en[name]} is standing here, looking menacing.",[]]
	],
	'hit': [
		["You swing your weapon. It connects!",[]],
		#{'message': "",
		#'substitutions':[]
		#}
		["You shoot {en[em]} for some damage.",[]]
	],
	'miss': [
		["Your swing goes wide.",[]],
		["You miss {en[em]} by a mile.",[]]
	],
	'enemy_hit': [
		["You are wounded by {en[eir]} vicious strike.",[]],
		["{en[Ey]} {words[0]} you.",[["hits","hit"]]]
	],
	'enemy_miss': [
		["{en[Ey]} {words[0]} to hit you, but {words[1]}. {en[Ey]} {words[2]} into the corner to cry.",[["tries","try"],["misses","miss"],["goes","go"]]],
		["You deftly dodge {en[eir]} {words[0]}.",[["attack","attacks"]]]
	],
}

#pronouns = {'em': ["him", "her", "it", "them"],
	#'ey': ["he", "she", "it", "they"].
	#'eir': ["his", "her", "its", "their"].
	#'emself': ["himself", "herself", "itself", "themselves"],
	#}

enemy = {'type': ["Giant", "Undead", "Kobold"],
	'name': "Billy-Joe",
	'em': "him",
	'ey': "he",
	'eir': "his",
	'emself': "himself",
	'Em': 'Him',
	'Ey': 'He',
	'Eir': 'His',
	'Emself': 'Himself',
	'plurality': 0
	}


def index(request):
	t = loader.get_template('main/index.djt')
	whomessage = random.choice(ref_strings['combat_status'])
	youmessage = random.choice(ref_strings['hit'])
	enemymessage = random.choice(ref_strings['enemy_miss'])
	c = Context({
			'combat_text': [
			whomessage[0].format(en=enemy, words=map(lambda x: x[enemy['plurality']], whomessage[1])),
			youmessage[0].format(en=enemy,words=map(lambda x: x[enemy['plurality']], youmessage[1])),
			enemymessage[0].format(en=enemy,words=map(lambda x: x[enemy['plurality']],enemymessage[1])),]
		})
	return HttpResponse(t.render(c))