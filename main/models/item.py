# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from JSONField import JSONField

class Item(models.Model):
	class Meta:
		app_label = 'main'
	name = models.CharField(max_length=50)
	article = models.CharField(max_length=20)
	multiplename = models.CharField(max_length=50)
	image_url = models.URLField()
	variety = JSONField()
	def __unicode__(self):
		return self.name

class MultiItem(models.Model):
	class Meta:
		app_label = 'main'
		abstract = True
	item = models.ForeignKey(Item)
	quantity = models.IntegerField()

class InventoryItem(MultiItem):
	class Meta:
		app_label = 'main'
	owner = models.ForeignKey('Hero', db_index=True)

	def add_item(cls, owner, item, quantity=1):
		try:
			prior = cls.objects.get(owner=owner, item=item)
			prior.quantity += quantity
			prior.save()
		except ObjectDoesNotExist:
			cls(owner=owner, item=item, quantity=quantity).save()
	add_item=classmethod(add_item)

class ItemDrop(MultiItem):
	class Meta:
		app_label = 'main'
	combat = models.ForeignKey('Combat', db_index=True)
	dropper = models.ForeignKey('Combatant')

	def add_item(cls, combat, dropper, item, quantity=1):
		try:
			prior = cls.objects.get(combat=combat, dropper=dropper, item=item)
			prior.quantity += quantity
			prior.save()
		except ObjectDoesNotExist:
			obj = ItemDrop(combat=combat, dropper=dropper, item=item, quantity=quantity)
			obj.save()
	add_item=classmethod(add_item)
