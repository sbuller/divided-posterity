# -*- coding: utf-8 -*-
from django.db import models

class CombatantSkill(models.Model):
	class Meta:
		app_label = 'main'
	skill = models.ForeignKey('Skill')
	mastery_level = models.IntegerField()
	slot = models.IntegerField()
	combatant = models.ForeignKey('Combatant')
