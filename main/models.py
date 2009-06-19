# -*- coding: utf-8 -*-
from django.db import models
from django.template import Context,Template

import json

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
	gender = models.CharField(max_length=1)#m/f/n/r

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
