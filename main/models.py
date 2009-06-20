# -*- coding: utf-8 -*-
from django.db import models
from django.template import Context,Template

import json, random

# Create your models here.

class Enemy(models.Model):
	"""
	>>> en = Enemy.objects.create(json_variety='["a","b","c"]',count=1)
	>>> en.variety
	u'a b c'
	"""
	json_variety = models.CharField(max_length=50)
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

	def _get_variety(self):
		return " ".join(json.loads(self.json_variety))
	variety = property(_get_variety)

class CombatMessage(models.Model):
	"""
	>>> message = CombatMessage.objects.create(message='Test {{en.name}} h{{en.count|pluralize:"i,ello"}}')
	>>> enemy = Enemy.objects.create(name='fred', count=1)
	>>> message.transmogrify(enemy)
	u'Test fred hi'
	"""
	action = models.CharField(max_length=50)
	message = models.TextField()

	def transmogrify(self, enemy):
		t = Template(self.message)
		c = Context({'en':enemy})
		return t.render(c)

class Item(models.Model):
	name = models.CharField(max_length=50)
	article = models.CharField(max_length=20)

class Location(models.Model):
	name = models.CharField(max_length=50)
	parent = models.ForeignKey('self', null=True, blank=True)
	json_platform = models.CharField(max_length=50)
	json_floor = models.CharField(max_length=50)
	json_wall = models.CharField(max_length=50)
	json_tool = models.CharField(max_length=50)
	json_hole = models.CharField(max_length=50)

	def _get_platform(self):
		return random.choice(json.loads(self.json_platform))

	def _get_floor(self):
		return random.choice(json.loads(self.json_floor))

	def _get_wall(self):
		return random.choice(json.loads(self.json_wall))

	def _get_tool(self):
		return random.choice(json.loads(self.json_tool))

	def _get_hole(self):
		return random.choice(json.loads(self.json_hole))

	platform = property(_get_platform)
	floor = property(_get_floor)
	wall = property(_get_wall)
	tool = property(_get_tool)
	hole = property(_get_hole)

	def __unicode__(self):
		return self.name
