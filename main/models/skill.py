# -*- coding: utf-8 -*-
from django.db import models
from action import Action

class Skill(models.Model):
	class Meta:
		app_label = 'main'
	name = models.CharField(max_length=50)
	action = models.ForeignKey(Action)
	image_url = models.URLField()

	def invoke(self, **kwargs):
		kwargs['context']={}
		exec(self.action.code, kwargs)
		if 'combat' in kwargs.keys() and 'action' in kwargs.keys():
			context = kwargs['context']
			context['actor'] = kwargs['actor']
			context['target'] = kwargs['target']
			context['combat'] = kwargs['combat']
			kwargs['combat'].add_message(kwargs['action'], context)

	def __unicode__(self):
		return self.name
