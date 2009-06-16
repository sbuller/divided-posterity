# -*- coding: utf-8 -*-
from django.db import models

import json

# Create your models here.

class Enemy(models.Model):
	json_variety = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	em = models.CharField(max_length=10)
	ey = models.CharField(max_length=10)
	eir = models.CharField(max_length=10)
	emself = models.CharField(max_length=10)
	cEm = models.CharField(max_length=10)
	cEy = models.CharField(max_length=10)
	cEir = models.CharField(max_length=10)
	cEmself = models.CharField(max_length=10)
	plurality = models.BooleanField()

	def _get_variety(self):
		return " ".join(json.loads(self.json_variety))
	variety = property(_get_variety)

class CombatMessage(models.Model):
	action = models.CharField(max_length=50)
	message = models.TextField()
	words = models.TextField()

	def transmogrify(self, enemy):
		return self.message.format(en=enemy, words=map(lambda x: x[enemy.plurality], json.loads(self.words)))

