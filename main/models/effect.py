# -*- coding: utf-8 -*-
from django.db import models

from combatant import Combatant

class Effect(models.Model):
	class Meta:
		app_label = 'main'
	name = models.CharField(max_length=50)

class EffectInstance(models.Model):
	class Meta:
		app_label = 'main'
	effect = models.ForeignKey(Effect)
	target = models.ForeignKey(Combatant)
	duration = models.IntegerField()
	unit = models.CharField(max_length=1, choices=(
		('a','Attack'),('c','Combat'),('d','Day'),('v','Adventure'),('r','Round of Combat')))