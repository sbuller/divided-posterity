# -*- coding: utf-8 -*-
from django.db import models

import random
from JSONField import JSONField
from PickledObjectField import PickledObjectField

from item import Item, InventoryItem
from message import Message
from combatant import Combatant

class Combat(models.Model):
	class Meta:
		app_label = 'main'
	turn = models.IntegerField(default=0)
	done = models.BooleanField(default=False)
	location = models.ForeignKey('Location')

	messages = JSONField()

	def enemies(self):
		return Combatant.objects.filter(combat=self,team__startswith="_enemy")

	def hero(self):
		return Combatant.objects.filter(combat=self, enemy__isnull=True)[0].hero

	def doitems(self):
		from item import ItemDrop
		winitems = ItemDrop.objects.filter(combat=self)
		for itemdrop in winitems:
			InventoryItem.add_item(self.hero(),itemdrop.item,itemdrop.quantity)

	def win(self):
		self.done = True
		for enemy in self.enemies():
			enemy.alive=False
			enemy.save()
			enemy.loot()
		self.doitems()
		hero = self.hero()
		if (hero.destination):
			hero.location = hero.destination
			hero.save()
		self.save()

	def won(self):
		surviving_enemies = Combatant.objects.filter(combat=self, alive=True, team__startswith="_enemy")
		return len(surviving_enemies) == 0

	def lose(self):
		self.done = True
		self.result = 'lost'
		self.save()

	def next_round(self):
		self.turn += 1
		who_message = random.choice(Message.objects.filter(action='who'))
		self.messages = [who_message.transmogrify({'en':self.enemies()[0].enemy, 'loc':self.location})]
		self.save()

	def addmessage(self, action, actor, target):
		message = random.choice(Message.objects.filter(action=action))
		self.messages.append(message.transmogrify({'actor':actor,'target':target, 'loc':self.location}))
		self.save()

	def challenger_hit(self):
		self.addmessage('attack hits',actor=self.hero(), target=self.enemies()[0])
	def challenger_miss(self):
		self.addmessage('attack misses',actor=self.hero(), target=self.enemies()[0])
	def opposition_hit(self):
		self.addmessage('attack hits',actor=self.enemies()[0], target=self.hero())
	def opposition_miss(self):
		self.addmessage('attack misses',actor=self.enemies()[0], target=self.hero())
		