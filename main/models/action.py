# -*- coding: utf-8 -*-
from django.db import models

class Action(models.Model):
	class Meta:
		app_label = 'main'
	code = models.TextField()

	def invoke(self, vars):
		exec(self.code, vars)