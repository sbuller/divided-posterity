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

	def _creaseness(self,stat):
		diff = self.__getattribute__(stat) - self.__getattribute__("base_"+stat)
		if diff<0:
			return "decreased"
		elif diff>0:
			return "increased"
		return "uncreased"
	tpl_brawn_change = lambda s: s._creaseness("brawn")
	tpl_charm_change = lambda s: s._creaseness("charm")
	tpl_finesse_change = lambda s: s._creaseness("finesse")
	tpl_lore_change = lambda s: s._creaseness("lore")
	tpl_magery_change = lambda s: s._creaseness("magery")
	tpl_stamina_change = lambda s: s._creaseness("stamina")

	def new_pvm_combat(self, enemy):
		return super(Hero,self).new_pvm_combat(enemy, self.destination)

	def __unicode__(self):
		return self.name + " " + self.family_name
