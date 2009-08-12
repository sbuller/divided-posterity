# -*- coding: utf-8 -*-
from django.db import models
from dp import settings

from enemy import Enemy

class NonCombat(models.Model):
	class Meta:
		app_label = 'main'

	name = models.CharField(max_length=50, null=True, blank=True)
	template_path = models.CharField(max_length=100)
	action = models.ForeignKey('Action', null=True, blank=True, related_name='action_noncombats')
	form_process = models.ForeignKey('Action', null=True, blank=True, related_name='form_noncombats')
	description = models.TextField()
	is_exclusive = models.BooleanField(default=True)

	@property
	def is_terminal(self):
		return self.form_process == None

	def __unicode__(self):
		return self.name

class EncounterInfo(models.Model):
	class Meta:
		app_label = 'main'

	encounter_rate = models.IntegerField()
	is_combat = models.BooleanField()

	enemy = models.ForeignKey('Enemy', null=True, blank=True)
	location = models.ForeignKey('Location', db_index=True)
	encounter = models.ForeignKey('NonCombat', null=True, blank=True)

	def __unicode__(self):
		if self.is_combat:
			return str(self.location) + ": " + self.enemy
		return str(self.location) + ": " + self.encounter
