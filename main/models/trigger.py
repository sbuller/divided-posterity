# -*- coding: utf-8 -*-
from django.db import models
from combatant import Combatant

class Trigger(models.Model):
	class Meta:
		app_label = 'main'
	combatant = models.ForeignKey(Combatant,blank=True,null=True)
	action = models.CharField(max_length=200,blank=True,null=True)
	trigger_name = models.CharField(max_length=50,blank=True,null=True)
	
	
def InvokeTriggers(trigger_name):
	all_triggers = Trigger.objects.filter(trigger_name=trigger_name)
	for trigger in all_triggers:
		print trigger.action