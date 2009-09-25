# -*- coding: utf-8 -*-
from django.db import models

class EquippedItem(models.Model):
	class Meta:
		app_label = 'main'
	item = models.ForeignKey('Item')
	hero = models.ForeignKey('Hero')
	
