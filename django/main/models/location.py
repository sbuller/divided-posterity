# -*- coding: utf-8 -*-
from django.db import models

from JSONField import JSONField

class Location(models.Model):
	class Meta:
		app_label = 'main'
	name = models.CharField(max_length=50)
	slug = models.CharField(max_length=50, primary_key=True)
	
	neighbors = models.ManyToManyField("self", blank=True)
	#encounters = models.ManyToManyField('Encounter', blank=True, through="EncounterInfo")
	
	platform = JSONField()
	floor = JSONField()
	wall = JSONField()
	tool = JSONField()
	hole = JSONField()

	def __unicode__(self):
		return self.name
