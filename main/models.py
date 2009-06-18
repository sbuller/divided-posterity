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
	em = models.CharField(max_length=10)
	ey = models.CharField(max_length=10)
	eir = models.CharField(max_length=10)
	eirs = models.CharField(max_length=10)
	emself = models.CharField(max_length=10)
	count = models.IntegerField()

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

