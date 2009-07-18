# -*- coding: utf-8 -*-
from django.db import models

class Action(models.Model):
	class Meta:
		app_label = 'main'
	code = models.TextField()

	def invoke(self, vars):
		exec(self.code, vars)

	@classmethod
	def generic_attack(cls, actor, target, stats={}):
		#case accuracy: True, attack hits, False: attack misses, else: roll some dice
		#case critical: True, critical hit, False: normal damage, else: roll some dice
		#case exact_damage: False: roll some dice, else: damage = exact_damage
		import random, math
		from main import Trigger
		DEFAULT_STATS = {
			"accuracy": actor.finesse,
			"critical": actor.lore,
			"exact_damage": False,
			"might": actor.brawn,
			"weap": 15, #actor.weapon_power
			"plus_damage": 0,
		}
		for k,v in DEFAULT_STATS:
			if not k in stats:
				stats[k] = v

		Trigger.invoke_triggers(target, "get attacked")
		Trigger.invoke_triggers(actor, "attack")
		if stats['accuracy'] != False:
			if stats['accuracy'] == True or stats['accuracy'] / target.charm >= 2 * random.random():
				pass
			else:
				return False
		else:
			return False

		if stats['exact_damage'] == False:
			damage = int(math.ceil(stats['might'] * stats['weapon'] / target.stamina * (0.8 + 0.4 * random.random())))
			damage += stats['plus_damage']
		else:
			damage = stats['exact_damage']

		if damage > 0:
			if stats['critical'] != False:
				if stats['critical'] == True or (stats['critical']-target.lore)/target.lore >= 4 * random.random():
					damage *= 1.5
			target.hp -= damage
			target.save()
			Trigger.invoke_triggers(target, "take damage")
			Trigger.invoke_triggers(actor, "deal damage")
		else:
			damage = 0

		return damage
