# -*- coding: utf-8 -*-
from django.db import models

from enemy import Enemy

class Encounter(models.Model):
	class Meta:
		app_label = 'main'
	name = models.CharField(max_length=50, null=True, blank=True)
	description = models.CharField(max_length=100)
	combatible = models.BooleanField()
	enemy = models.ForeignKey(Enemy, null=True, blank=True)
	def __unicode__(self):
		return self.name or ("Battle of " + self.enemy.name)

class EncounterInfo(models.Model):
	class Meta:
		app_label = 'main'
	encounterrate = models.IntegerField()
	location = models.ForeignKey('Location')
	encounter = models.ForeignKey(Encounter)
