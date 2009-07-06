# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from combatant import Combatant

class Hero(Combatant):
	class Meta:
		app_label = 'main'
	name = models.CharField(max_length=50)
	variety = models.CharField(max_length=50)
	family_name = models.CharField(max_length=50)
	user = models.ForeignKey(User, db_index=True)

	base_brawn = models.IntegerField()
	base_charm = models.IntegerField()
	base_finesse = models.IntegerField()
	base_lore = models.IntegerField()
	base_magery = models.IntegerField()
	base_stamina = models.IntegerField()

	destination = models.ForeignKey('Location', null=True, blank=True, related_name='incoming_heroes')
	location = models.ForeignKey('Location', default='tree_village', related_name='populace')

	inventory = models.ManyToManyField('Item', through='InventoryItem')

	def new_pvm_combat(self, enemy):
		return super(Hero,self).new_pvm_combat(enemy, self.destination)

	def __unicode__(self):
		return self.name + " " + self.family_name
