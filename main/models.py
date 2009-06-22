# -*- coding: utf-8 -*-
from django.db import models
from django.template import Context,Template

import json, random
from JSONField import JSONField

# Create your models here.

class Enemy(models.Model):
	"""
	>>> en = Enemy.objects.create(json_variety='["a","b","c"]',count=1)
	>>> en.variety
	u'a b c'
	"""
	variety = JSONField(max_length=50)
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
	action = models.CharField(max_length=50)
	message = models.TextField()

	def transmogrify(self, enemy, location):
		t = Template(self.message)
		c = Context({'en':enemy, 'loc':location})
		return t.render(c)

class Item(models.Model):
	name = models.CharField(max_length=50)
	article = models.CharField(max_length=20)

class Location(models.Model):
	name = models.CharField(max_length=50)
	parent = models.ForeignKey('self', null=True, blank=True)
	platform = JSONField(max_length=50)
	floor = JSONField(max_length=50)
	wall = JSONField(max_length=50)
	tool = JSONField(max_length=50)
	hole = JSONField(max_length=50)

	def __unicode__(self):
		return self.name

class Combat:
	def __init__(self):
		enemy = random.choice(Enemy.objects.all())
		self.enemy = enemy
		self.turn = 0
		self.done = False

	def win(self):
		self.done = True
		self.result = 'won'

	def lose(self):
		self.done = True
		self.result = 'lost'

	def next_round(self):
		self.turn += 1
		self._youhit = False
		self._theyhit = False

	def youhit(self):
		self._youhit = True
		pass
	def youmiss(self):
		pass
	def theyhit(self):
		self._theyhit = True
		pass
	def theymiss(self):
		pass
