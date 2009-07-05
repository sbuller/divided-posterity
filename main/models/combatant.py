# -*- coding: utf-8 -*-
from django.db import models

from skill import Skill

class Combatant(models.Model):
	class Meta:
		app_label = 'main'
	enemy = models.ForeignKey('Enemy', null=True, blank=True, db_index=True)

	team = models.CharField(max_length=50, default="_enemy")

	brawn = models.IntegerField()
	charm = models.IntegerField()
	finesse = models.IntegerField()
	lore = models.IntegerField()
	magery = models.IntegerField()
	stamina = models.IntegerField()

	effects = models.ManyToManyField('Effect', through='EffectInstance')
	skills = models.ManyToManyField(Skill)
	combat = models.ForeignKey('Combat', blank=True, null=True)

	def new_pvm_combat(self, enemy, location):
		from combat import Combat
		c = Combat(location=location)
		c.save()
		oldcombat = self.combat
		self.combat = c
		enemy.new_combatant(combat=c)
		self.save()
		if oldcombat:
			oldcombat.delete()
		return c

	def __unicode__(self):
		try:
			return self.hero.__unicode__()
		except:
			return self.enemy.__unicode__()
