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
	winitems = PickledObjectField()

	messages = JSONField()

	def enemies(self):
		return Combatant.objects.filter(combat=self,team__startswith="_enemy")

	def hero(self):
		return Combatant.objects.filter(combat=self, enemy__isnull=True)[0].hero

	def doitems(self):
		winitems = {}
		winitems[random.choice(Item.objects.all())] = 1
		while random.choice([True,False]):
			item = random.choice(Item.objects.all())
			if not item in winitems:
				winitems[item] = 1
			else:
				winitems[item] += 1
		for key,value in winitems.iteritems():
			InventoryItem.add_item(self.hero(),key,value)
		self.winitems = winitems
		self.save()

	def win(self):
		self.done = True
		self.doitems()
		for enemy in self.enemies():
			enemy.delete()
		hero = self.hero()
		if (hero.destination):
			hero.location = hero.destination
			hero.save()
		self.save()

	def won(self):
		return len(self.enemies()) == 0

	def lose(self):
		self.done = True
		self.result = 'lost'
		self.save()

	def next_round(self):
		self.turn += 1
		who_message = random.choice(Message.objects.filter(action='who'))
		self.messages = [who_message.transmogrify({'en':self.enemies()[0].enemy, 'loc':self.location})]
		self.save()

	def addmessage(self, action):
		message = random.choice(Message.objects.filter(action=action))
		self.messages.append(message.transmogrify({'en':self.enemies()[0].enemy, 'loc':self.location}))
		self.save()

	def challenger_hit(self): self.addmessage('you hit')
	def challenger_miss(self): self.addmessage('you miss')
	def opposition_hit(self): self.addmessage('enemy hits')
	def opposition_miss(self): self.addmessage('enemy misses')
