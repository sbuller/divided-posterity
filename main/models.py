# -*- coding: utf-8 -*-
from django.db import models
from django.template import Context,Template

import json

# Create your models here.

class Enemy(models.Model):
	"""
	>>> en = Enemy.objects.create(json_variety='["a","b","c"]')
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
	cEm = models.CharField(max_length=10)
	cEy = models.CharField(max_length=10)
	cEir = models.CharField(max_length=10)
	cEirs = models.CharField(max_length=10)
	cEmself = models.CharField(max_length=10)
	plurality = models.BooleanField()

	def _get_variety(self):
		return " ".join(json.loads(self.json_variety))
	variety = property(_get_variety)

class CombatMessage(models.Model):
	"""
	>>> message = CombatMessage.objects.create(message="Test {{en.name}} {{words.0}}",json_words='[["hi","hello"]]')
	>>> enemy = Enemy.objects.create(name='fred',plurality=0)
	>>> message.transmogrify(enemy)
	u'Test fred hi'
	"""
	action = models.CharField(max_length=50)
	message = models.TextField()
	json_words = models.TextField()

	def _get_words(self):
		return json.loads(self.json_words)
	words = property(_get_words)

	def transmogrify(self, enemy):
		t = Template(self.message)
		words = map(lambda x: x[enemy.plurality], self.words)
		c = Context({'en':enemy, 'words':words})
		return t.render(c)

