# -*- coding: utf-8 -*-
from django.db import models

import random
from JSONField import JSONField
from PickledObjectField import PickledObjectField

from item import Item, InventoryItem
from message import Message

class Combat(models.Model):
	class Meta:
		app_label = 'main'
	challenger = models.OneToOneField('Combatant', related_name="challenger_combat", blank=True, null=True, db_index=True)
	opposition = models.OneToOneField('Combatant', related_name="opposition_combat", blank=True, null=True)
	turn = models.IntegerField(default=0)
	done = models.BooleanField(default=False)
	location = models.ForeignKey('Location')
	winitems = PickledObjectField()

	messages = JSONField()

	def win(self):
		winitems = {}
		winitems[random.choice(Item.objects.all())] = 1
		while random.choice([True,False]):
			item = random.choice(Item.objects.all())
			if not item in winitems:
				winitems[item] = 1
			else:
				winitems[item] += 1
		for key,value in winitems.iteritems():
			InventoryItem.add_item(self.challenger.hero,key,value)
		self.done = True
		self.winitems = winitems
		self.result = 'won'
		hero = self.challenger.hero
		if (hero.destination):
			hero.location = hero.destination
			#hero.destination = None
			hero.save()
		self.save()

	def won(self):
		return self.result == 'won'

	def lose(self):
		self.done = True
		self.result = 'lost'
		#self.challenger.hero.update(destination=None)
		self.save()

	def next_round(self):
		self.turn += 1
		who_message = random.choice(Message.objects.filter(action='who'))
		self.messages = [who_message.transmogrify({'en':self.opposition.enemy, 'loc':self.location})]
		self.save()

	def addmessage(self, action):
		message = random.choice(Message.objects.filter(action=action))
		self.messages.append(message.transmogrify({'en':self.opposition.enemy, 'loc':self.location}))
		self.save()

	def challenger_hit(self): self.addmessage('you hit')
	def challenger_miss(self): self.addmessage('you miss')
	def opposition_hit(self): self.addmessage('enemy hits')
	def opposition_miss(self): self.addmessage('enemy misses')
