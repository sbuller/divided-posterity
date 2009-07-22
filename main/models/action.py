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
	def damage(cls, target, amount, actor=None):
		from trigger import Trigger
		target.hp -= amount
		target.save()
		print "damage:",amount,"target:",target,"hp left:",target.hp
		Trigger.invoke_triggers(target, "receive damage")
		if actor:
			Trigger.invoke_triggers(actor, "deal damage")

	@classmethod
	def generic_attack(cls, actor, target, stats={}):
		'''
		returns damage dealt (None on miss)
		case accuracy: 'Inf', attack hits, None: attack misses, else: roll some dice
		case critical: 'Inf', critical hit, None: normal damage, else: roll some dice
		case exact_damage: None: roll some dice, else: damage = exact_damage
		'''
		import random, math
		from trigger import Trigger
		DEFAULT_STATS = {
			"accuracy": actor.finesse,
			"critical": actor.lore,
			"exact_damage": None,
			"might": actor.brawn,
			"weapon": 3, #actor.weapon_power
			"plus_damage": 0,
		}
		stats_in = stats
		stats = DEFAULT_STATS.copy()
		stats.update(stats_in)

		#print "actor:", actor, "target:", target
		#print "stats:", stats

		Trigger.invoke_triggers(target, "receive attack")
		Trigger.invoke_triggers(actor, "deal attack")
		if (stats['accuracy'] != None) and (float(stats['accuracy']) * 2.0 / 3.0 / target.charm >= random.random()):
			Trigger.invoke_triggers(target, "receive hit")
			Trigger.invoke_triggers(actor, "deal hit")
		else:
			Trigger.invoke_triggers(target, "receive miss")
			Trigger.invoke_triggers(actor, "deal miss")
			return None

		if stats['exact_damage'] == None:
			damage = int(math.ceil(stats['might'] * stats['weapon'] * (0.8 + 0.4 * random.random()) / target.stamina))
			damage += stats['plus_damage']
		else:
			damage = stats['exact_damage']

		if damage > 0:
			if stats['critical'] != None:
				if 0.25 * (float(stats['critical'])-target.lore)/target.lore >= random.random():
					damage = int(math.ceil(damage * 1.5))
			Action.damage(target, damage)
		else:
			damage = 0

		return damage

	def __unicode__(self):
		return self.name
