# -*- coding: utf-8 -*-
from django.db import models
from action import Action

class Skill(models.Model):
	class Meta:
		app_label = 'main'
	name = models.CharField(max_length=50)
	action = models.ForeignKey(Action,null=True)
	image_url = models.URLField()

	def __unicode__(self):
		return self.name
