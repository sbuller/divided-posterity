# -*- coding: utf-8 -*-
from django.db import models
from combatant import Combatant
from JSONField import JSONField

class Trigger(models.Model):
	class Meta:
		app_label = 'main'
	combatant = models.ForeignKey(Combatant,blank=True,null=True)
	action = models.ForeignKey('Action')
	value = JSONField()
	trigger_name = models.CharField(max_length=50)

def InvokeTriggers(trigger_name):
	all_triggers = Trigger.objects.filter(trigger_name=trigger_name)
	for trigger in all_triggers:
		exec(trigger.action.code, trigger.value)
