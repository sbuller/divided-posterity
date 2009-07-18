# -*- coding: utf-8 -*-
from django.db import models
from combatant import Combatant
from JSONField import JSONField

class Trigger(models.Model):
	class Meta:
		app_label = 'main'
	combatant = models.ForeignKey(Combatant, db_index=True)
	action = models.ForeignKey('Action')
	value = JSONField()
	trigger_name = models.CharField(max_length=50, db_index=True)
	effect = models.ForeignKey('Effect', blank=True, null=True)
	combat = models.ForeignKey('Combat', blank=True, null=True)

	@classmethod
	def invoke_triggers(cls, combatant, trigger_name):
		all_triggers = Trigger.objects.filter(combatant=combatant, trigger_name=trigger_name)
		for trigger in all_triggers:
			trigger.value['combatant'] = combatant
			exec(trigger.action.code, trigger.value)
