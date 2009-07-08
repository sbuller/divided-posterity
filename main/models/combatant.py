# -*- coding: utf-8 -*-
from django.db import models

from skill import Skill

class Combatant(models.Model):
	class Meta:
		app_label = 'main'
	enemy = models.ForeignKey('Enemy', null=True, blank=True, db_index=True)

	team = models.CharField(max_length=50, default="_enemy")

	gender = models.CharField(max_length=1, choices=(('m','Male'),('f','Female'),('n','Neutral'),('r','Randomly male or female')))
	count = models.IntegerField(default=1)
	
	brawn = models.IntegerField()
	charm = models.IntegerField()
	finesse = models.IntegerField()
	lore = models.IntegerField()
	magery = models.IntegerField()
	stamina = models.IntegerField()

	effects = models.ManyToManyField('Effect', through='EffectInstance')
	skills = models.ManyToManyField(Skill)
	combat = models.ForeignKey('Combat', blank=True, null=True, db_index=True)

	alive = models.BooleanField(default=True)

	player_pov = False
	
	def base_stat(self, stat):
		try:
			return self.hero.__getattribute__("base_"+stat)
		except:
			return self.enemy.__getattribute__("base_"+stat)
	bbrawn = property(lambda s: s.base_stat("brawn"))
	bcharm = property(lambda s: s.base_stat("charm"))
	bfinesse = property(lambda s: s.base_stat("finesse"))
	blore = property(lambda s: s.base_stat("lore"))
	bmagery = property(lambda s: s.base_stat("magery"))
	bstamina = property(lambda s: s.base_stat("stamina"))

	def _modify(self, value, base_stat, function="c"):
		if function == 'c':
			return value
		elif function == 'x':
			return value * base_stat
		else:
			return 0

	def update_vars(self, variables = ['brawn','charm','finesse','lore','magery','stamina']):
		from effect import Modifier
		from django.db.models import Q
		import math
		query = None
		tot = {}
		for var in variables:
			if var in ['brawn','charm','finesse','lore','magery','stamina']:
				tot[var] = 0
				if query is None:
					query = Q(variable=var)
				else:
					query |= Q(variable=var)
		if query is None:
			query = Q(combatant=self)
		else:
			query &= Q(combatant=self)
		mods = Modifier.objects.filter(query)
		for mod in mods:
			tot[mod.variable] += self._modify(mod.value, self.__getattribute__("b"+mod.variable), mod.function)
		for k in tot.keys():
			self.__setattr__(k, self.__getattribute__("b"+k) + int(math.ceil(tot[k])))
		self.save()

	def update_var(self, variable):
		from effect import Modifier
		import math
		if variable in ['brawn','charm','finesse','lore','magery','stamina']:
			mods = Modifier.objects.filter(combatant=self, variable=variable)
			tot = 0
			for mod in mods:
				tot += self._modify(mod.value, self.__getattribute__("b"+variable), mod.function)
			self.__setattr__(variable, self.__getattribute__("b"+variable) + int(math.ceil(tot)))
			self.save()

	def new_pvm_combat(self, enemy, location):
		from combat import Combat
		c = Combat(location=location)
		c.save()
		oldcombat = self.combat
		self.combat = c
		enemy.new_combatant(combat=c)
		self.save()
		if oldcombat:
			oldcombat.delete()
		return c

	def loot(self):
		try:
			self.hero.loot(self.combat)
		except:
			self.enemy.loot(self.combat, self)

	def spoils(self):
		from item import ItemDrop
		return ItemDrop.objects.filter(combat=self.combat)

	def __unicode__(self):
		try:
			return self.hero.__unicode__()
		except:
			return self.enemy.__unicode__()
