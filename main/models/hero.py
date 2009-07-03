# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

class Hero(models.Model):
	class Meta:
		app_label = 'main'
	name = models.CharField(max_length=50)
	variety = models.CharField(max_length=50)
	family_name = models.CharField(max_length=50)
	gender = models.CharField(max_length=1, choices=(('m','Male'),('f','Female')))
	user = models.ForeignKey(User, db_index=True)

	base_brawn = models.IntegerField()
	base_charm = models.IntegerField()
	base_finesse = models.IntegerField()
	base_lore = models.IntegerField()
	base_magery = models.IntegerField()
	base_stamina = models.IntegerField()

	destination = models.ForeignKey('Location', null=True, blank=True, related_name='incoming_heroes')
	location = models.ForeignKey('Location', default='tree_village', related_name='populace')
	combatant = models.OneToOneField('Combatant', db_index=True, blank=True, null=True)

	inventory = models.ManyToManyField('Item', through='InventoryItem')

	def new_pvm_combat(self, enemy):
		return self.combatant.new_pvm_combat(enemy, self.destination)

	def _new_combatant(self):
		if (not self.combatant):
			from combatant import Combatant
			c = Combatant(enemy=None, brawn=self.base_brawn,
				charm=self.base_charm, finesse=self.base_finesse,
				lore=self.base_lore, magery=self.base_magery,
				stamina=self.base_stamina)
			c.save()
			self.combatant = c
			self.save()
			return c

	def __unicode__(self):
		return self.name + " " + self.family_name
def make_hero_combatant(sender, instance, **kwargs):
	instance._new_combatant()
pre_save.connect(make_hero_combatant, sender=Hero)
