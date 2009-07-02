# -*- coding: utf-8 -*-
from django.db import models

from enemy import Enemy

class Encounter(models.Model):
	class Meta:
		app_label = 'main'
		
	name = models.CharField(max_length=50, null=True, blank=True)
	description = models.CharField(max_length=500)
	
	def __unicode__(self):
		return self.name

class EncounterInfo(models.Model):
	class Meta:
		app_label = 'main'
		
	encounter_rate = models.IntegerField()
	is_combat = models.BooleanField()
	
	enemy = models.ForeignKey('Enemy', null=True, blank=True)
	location = models.ForeignKey('Location', db_index=True)
	encounter = models.ForeignKey('Encounter', null=True, blank=True)
	
	def __unicode__(self):
		if self.is_combat:
			return self.location + ": " + self.enemy
		return self.location + ": " + self.encounter
