# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

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

	hp = models.IntegerField(blank=True, null=True)
	max_hp = models.IntegerField(blank=True, null=True)

	mp = models.IntegerField(blank=True, null=True)
	max_mp = models.IntegerField(blank=True, null=True)

	effects = models.ManyToManyField('Effect', through='EffectInstance')
	skills = models.ManyToManyField('Skill', through='CombatantSkill')
	combat = models.ForeignKey('Combat', blank=True, null=True, db_index=True)

	alive = models.BooleanField(default=True)

	player_pov = False

	#Django already overrides this function, so it sort of breaks things.
	#def __getattr__(self, name):
		#try:
			#return self.entity.__getattribute__(name)
		#except ObjectDoesNotExist:
			#return super(Combatant,self).__getattr__(name)

	def _get_entity(self):
		try:
			return self.hero
		except:
			return self.enemy
	entity = property(_get_entity)

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
		tot = {}
		for var in variables:
				tot[var] = 0
		mods = Modifier.objects.filter(Q(variable__in=variables)&Q(combatant=self))
		for mod in mods:
			tot[mod.variable] += self._modify(mod.value, self.entity.__getattribute__("base_"+mod.variable), mod.function)
		for k in tot.keys():
			self.__setattr__(k, self.entity.__getattribute__("base_"+k) + int(math.ceil(tot[k])))
		self.save()

	def update_var(self, variable):
		from effect import Modifier
		import math
		if variable in ['brawn','charm','finesse','lore','magery','stamina']:
			mods = Modifier.objects.filter(combatant=self, variable=variable)
			tot = 0
			for mod in mods:
				tot += self._modify(mod.value, self.entity.__getattribute__("base_"+variable), mod.function)
			self.__setattr__(variable, self.entity.__getattribute__("base_"+variable) + int(math.ceil(tot)))
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
		c.init_combat()
		c.next_round()
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
