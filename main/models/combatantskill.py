# -*- coding: utf-8 -*-
from django.db import models

class CombatantSkill(models.Model):
	class Meta:
		app_label = 'main'
	skill = models.ForeignKey('Skill', db_index=True)
	mastery_level = models.IntegerField(default=1)
	slot = models.IntegerField(blank=True,null=True)
	combatant = models.ForeignKey('Combatant', db_index=True)
