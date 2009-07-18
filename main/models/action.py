# -*- coding: utf-8 -*-
from django.db import models

class Action(models.Model):
	class Meta:
		app_label = 'main'
	code = models.TextField()
	name = models.CharField(max_length=50)

	def invoke(self, vars):
		exec(self.code, vars)

	@classmethod
	def generic_attack(cls, actor, target, stats={}):
		#returns damage dealt (False on miss)
		#case accuracy: True, attack hits, False: attack misses, else: roll some dice
		#case critical: True, critical hit, False: normal damage, else: roll some dice
		#case exact_damage: False: roll some dice, else: damage = exact_damage
		import random, math
		from trigger import Trigger
		DEFAULT_STATS = {
			"accuracy": actor.finesse,
			"critical": actor.lore,
			"exact_damage": False,
			"might": actor.brawn,
			"weapon": 3, #actor.weapon_power
			"plus_damage": 0,
		}
		for k in DEFAULT_STATS.keys():
			if not k in stats:
				stats[k] = DEFAULT_STATS[k]

		Trigger.invoke_triggers(target, "receive attack")
		Trigger.invoke_triggers(actor, "deal attack")
		if stats['accuracy'] != False and (stats['accuracy'] == True or stats['accuracy'] * 2.0 / 3.0 / target.charm >= random.random()):
			Trigger.invoke_triggers(target, "receive hit")
			Trigger.invoke_triggers(actor, "deal hit")
		else:
			Trigger.invoke_triggers(target, "receive miss")
			Trigger.invoke_triggers(actor, "deal miss")
			return False

		if stats['exact_damage'] == False:
			damage = int(math.ceil(stats['might'] * stats['weapon'] * (0.8 + 0.4 * random.random()) / target.stamina))
			damage += stats['plus_damage']
		else:
			damage = stats['exact_damage']

		if damage > 0:
			if stats['critical'] != False:
				if stats['critical'] == True or 0.25 * (stats['critical']-target.lore)/target.lore >= random.random():
					damage *= 1.5
			target.hp -= damage
			target.save()
			Trigger.invoke_triggers(target, "receive damage")
			Trigger.invoke_triggers(actor, "deal damage")
		else:
			damage = 0

		return damage
