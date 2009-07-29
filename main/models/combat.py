# -*- coding: utf-8 -*-
from django.db import models

import random
from JSONField import JSONField
from PickledObjectField import PickledObjectField

from item import Item, InventoryItem
from message import Message
from combatant import Combatant
from trigger import Trigger

class Combat(models.Model):
	class Meta:
		app_label = 'main'
	turn = models.IntegerField(default=0)
	done = models.BooleanField(default=False)
	location = models.ForeignKey('Location')

	messages = JSONField()

	def teams_alive(self):
		all_teams = [team for team in map(lambda x: x.__getattribute__("team"), self.combatants().filter(alive=True))]
		teams = {}
		for team in all_teams:
			if not team in teams:
				teams[team] = 1
			else:
				teams[team] += 1
		return teams

	def enemies(self):
		return Combatant.objects.filter(combat=self,team__startswith="_enemy")

	def heros(self):
		from hero import Hero
		return Hero.objects.filter(combat=self)

	def combatants(self):
		return Combatant.objects.filter(combat=self)

	def doitems(self):
		from item import ItemDrop
		winitems = ItemDrop.objects.filter(combat=self)
		for itemdrop in winitems:
			InventoryItem.add_item(self.heros()[0],itemdrop.item,itemdrop.quantity)

	def win(self, winning_team):
		self.done = True
		for enemy in self.enemies().exclude(team=winning_team):
			enemy.loot()
		self.doitems()
		hero = self.heros()[0]
		if (hero.destination):
			hero.location = hero.destination
			hero.save()
		self.award_exp(hero)
		self.save()

	def award_exp(self, hero):
		old_stats = {
			"brawn": hero.base_brawn,
			"charm": hero.base_charm,
			"finesse": hero.base_finesse,
			"lore": hero.base_lore,
			"magery": hero.base_magery,
			"stamina":  hero.base_stamina
		}
		d = {"brawn":0, "charm":0, "finesse":0, "lore":0, "magery":0, "stamina":0}
		exp = hero.add_experience(sum(map(lambda s: s.__getattribute__("max_hp"), self.enemies().all())))
		d.update(exp)
		for k,v in d.items():
			hero.__dict__[k+"_exp_gain"] = v
			hero.__dict__[k+"_up"] = hero.__dict__["base_"+k] - old_stats[k]
		hero.save()

	def won(self):
		surviving_enemies = Combatant.objects.filter(combat=self, alive=True, team__startswith="_enemy")
		return len(surviving_enemies) == 0

	def lose(self):
		self.done = True
		self.result = 'lost'
		self.save()

	def init_combat(self):
		from hero import Hero
		from action import Action
		act = Action.objects.filter(name="die?").all()[0]
		for hero in self.heros():
			hero.max_hp = hero.base_brawn + hero.base_charm + hero.base_finesse + hero.base_lore + hero.base_magery + hero.base_stamina
			hero.hp = hero.max_hp
			hero.max_mp = max(10, hero.max_hp/4)
			hero.mp = 0
			hero.alive = True
			hero.save()
			Trigger(combatant = hero, trigger_name="receive damage", action=act, combat=self, value={}).save()
		for en in self.enemies():
			en.max_hp = en.enemy.base_brawn + en.enemy.base_charm + en.enemy.base_finesse + en.enemy.base_lore + en.enemy.base_magery + en.enemy.base_stamina
			en.hp = en.max_hp
			en.max_mp = max(10, en.max_hp/4)
			en.mp = 0
			en.alive = True
			en.save()
			Trigger(combatant = en, trigger_name="receive damage", action=act, combat=self, value={}).save()

	def next_round(self):
		from main.utils import distribute
		self.turn += 1
		self.save()
		for hero in self.heros():
			hero.combat_messages.append([])
			hero.save()
		combatants = Combatant.objects.filter(combat=self, alive=True).all()
		magerys = map(lambda s: s.__getattribute__("magery"), combatants)
		num_mp = 5 * len(combatants)
		mp_gains = distribute(num_mp, magerys)
		for i in xrange(len(combatants)):
			combatants[i].mp = min(combatants[i].max_mp, combatants[i].mp + mp_gains[i])
			combatants[i].save()
			Trigger.invoke_triggers(combatants[i], "end of round")


	def add_message(self, action, context):
		message = random.choice(Message.objects.filter(action=action))
		for hero in self.heros():
			hero.combat_messages[self.turn].append(message.transmogrify(context, pov=hero))
			hero.save()
		self.save()
