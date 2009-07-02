# -*- coding: utf-8 -*-
from django.db import models

from skill import Skill

class Combatant(models.Model):
	class Meta:
		app_label = 'main'
	enemy = models.ForeignKey('Enemy', null=True, blank=True, db_index=True)

	brawn = models.IntegerField()
	charm = models.IntegerField()
	finesse = models.IntegerField()
	lore = models.IntegerField()
	magery = models.IntegerField()
	stamina = models.IntegerField()

	effects = models.ManyToManyField('Effect', through='EffectInstance')
	skills = models.ManyToManyField(Skill)

	def _get_hero(self):
		from hero import Hero
		if Hero.objects.filter(combatant=self):
			return Hero.objects.filter(combatant=self)[0]
		return None
	hero = property(_get_hero)

	def __unicode__(self):
		return (self.hero or self.enemy).__unicode__()
