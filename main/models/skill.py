# -*- coding: utf-8 -*-
from django.db import models

class Skill(models.Model):
	class Meta:
		app_label = 'main'
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name
