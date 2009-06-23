# -*- coding: utf-8 -*-
from django.db import models
from django.template import Context,Template
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

import json, random
from JSONField import JSONField

# Create your models here.

class Enemy(models.Model):
	"""
	>>> en = Enemy.objects.create(json_variety='["a","b","c"]',count=1)
	>>> en.variety
	u'a b c'
	"""
	variety = JSONField()
	name = models.CharField(max_length=50)
	count = models.IntegerField()
	gender = models.CharField(max_length=1, choices=(('m','Male'),('f','Female'),('n','Neutral'),('r','Randomly male or female')))

	def unspivak(self, x):
		table = [ #m,f,n,p
			['him','her','it','them'], #em
			['he','she','it','they'], #ey
			['his','her','its','their'], #eir
			['his','hers','its','theirs'], #eirs
			['himself','herself','itself','themselves'] #emself
		]
		gender = ['m','f','n','p']
		val = table[x][(3,gender.index(self.gender))[not self.count-1]]
		return val
	em = property(lambda s: s.unspivak(0))
	ey = property(lambda s: s.unspivak(1))
	eir = property(lambda s: s.unspivak(2))
	eirs = property(lambda s: s.unspivak(3))
	emself = property(lambda s: s.unspivak(4))

class CombatMessage(models.Model):
	"""
	>>> message = CombatMessage.objects.create(message='Test {{en.name}} h{{en.count|pluralize:"i,ello"}}')
	>>> enemy = Enemy.objects.create(name='fred', count=1)
	>>> message.transmogrify(enemy)
	u'Test fred hi'
	"""
	action = models.CharField(max_length=50, db_index=True)
	message = models.TextField()

	def transmogrify(self, enemy, location):
		t = Template(self.message)
		c = Context({'en':enemy, 'loc':location})
		return t.render(c)

class Item(models.Model):
	name = models.CharField(max_length=50)
	article = models.CharField(max_length=20)
	def __unicode__(self):
		return self.name

class Location(models.Model):
	name = models.CharField(max_length=50)
	parent = models.ForeignKey('self', null=True, blank=True, db_index=True)
	enemies = models.ManyToManyField(Enemy)
	platform = JSONField()
	floor = JSONField()
	wall = JSONField()
	tool = JSONField()
	hole = JSONField()

	def __unicode__(self):
		return self.name

class Combat:
	def __init__(self, location):
		enemy = random.choice(Enemy.objects.all())
		self.enemy = enemy
		self.turn = 0
		self.done = False
		self.location = location

	def win(self):
		self.done = True
		self.result = 'won'

	def won(self):
		return self.result == 'won'

	def lose(self):
		self.done = True
		self.result = 'lost'

	def next_round(self):
		self.turn += 1
		who_message = random.choice(CombatMessage.objects.filter(action='who'))
		self.messages = [who_message.transmogrify(self.enemy, self.location)]

	def youhit(self):
		you_message = random.choice(CombatMessage.objects.filter(action='you hit'))
		self.messages.append(you_message.transmogrify(self.enemy, self.location))

	def youmiss(self):
		you_message = random.choice(CombatMessage.objects.filter(action='you miss'))
		self.messages.append(you_message.transmogrify(self.enemy, self.location))

	def theyhit(self):
		you_message = random.choice(CombatMessage.objects.filter(action='enemy hits'))
		self.messages.append(you_message.transmogrify(self.enemy, self.location))

	def theymiss(self):
		you_message = random.choice(CombatMessage.objects.filter(action='enemy misses'))
		self.messages.append(you_message.transmogrify(self.enemy, self.location))


class InventoryItem(models.Model):
	owner = models.ForeignKey(User, db_index=True)
	item = models.ForeignKey(Item)
	quantity = models.IntegerField()

	def add_item(cls, owner, item, quantity=1):
		try:
			prior = cls.objects.get(owner=owner, item=item)
			prior.quantity += quantity
			prior.save()
		except ObjectDoesNotExist:
			cls(owner=owner, item=item, quantity=quantity).save()
	add_item=classmethod(add_item)

	def __unicode__(self):
		return self.owner.username + "'s " + self.item.name + "(s)"
