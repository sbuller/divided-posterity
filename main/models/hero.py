# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from combatant import Combatant
from JSONField import JSONField

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

	brawn_exp = models.IntegerField(default=0)
	charm_exp = models.IntegerField(default=0)
	finesse_exp = models.IntegerField(default=0)
	lore_exp = models.IntegerField(default=0)
	magery_exp = models.IntegerField(default=0)
	stamina_exp = models.IntegerField(default=0)

	brawn_exp_gain = models.IntegerField(default=0)
	charm_exp_gain = models.IntegerField(default=0)
	finesse_exp_gain = models.IntegerField(default=0)
	lore_exp_gain = models.IntegerField(default=0)
	magery_exp_gain = models.IntegerField(default=0)
	stamina_exp_gain = models.IntegerField(default=0)

	combat_messages = JSONField()

	non_combat = models.ForeignKey('NonCombat', null=True, blank=True)

	#equipped_items = models.ManyToManyField('Item',through='EquippedItem')

	destination = models.ForeignKey('Location', null=True, blank=True, related_name='incoming_heroes')
	location = models.ForeignKey('Location', default='tree_village', related_name='populace')

	inventory = models.ManyToManyField('Item', through='InventoryItem')

	def total_exp_gain(self):
		return self.brawn_exp_gain + self.charm_exp_gain + self.finesse_exp_gain + self.lore_exp_gain + self.magery_exp_gain + self.stamina_exp_gain

	def _stat_up(self, stat):
		upness = 0
		remainder = self.__dict__[stat+"_exp_gain"]
		value = self.__dict__["base_"+stat]
		exp = self.__dict__[stat+"_exp"]
		while remainder > exp:
			upness += 1
			remainder -= value * 2 - 1
			value -= 1
			exp = value * 2 - 1
		return upness
	brawn_up = property(lambda s: s._stat_up("brawn"))
	charm_up = property(lambda s: s._stat_up("charm"))
	finesse_up = property(lambda s: s._stat_up("finesse"))
	lore_up = property(lambda s: s._stat_up("lore"))
	magery_up = property(lambda s: s._stat_up("magery"))
	stamina_up = property(lambda s: s._stat_up("stamina"))
	
	def _max_stat_exp(self, stat):
		return 2 * self.__dict__["base_"+stat] + 1
	max_brawn_exp = property(lambda s: s._max_stat_exp("brawn"))
	max_charm_exp = property(lambda s: s._max_stat_exp("charm"))
	max_finesse_exp = property(lambda s: s._max_stat_exp("finesse"))
	max_lore_exp = property(lambda s: s._max_stat_exp("lore"))
	max_magery_exp = property(lambda s: s._max_stat_exp("magery"))
	max_stamina_exp = property(lambda s: s._max_stat_exp("stamina"))

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

	def add_experience(self, d, stat=None):
		if isinstance(d, dict):
			d2 = []
			for s, amt in d.items():
				self.__dict__[s+"_exp"] += amt
				while self.__dict__[s+"_exp"] >= 2 * self.__dict__["base_"+s] + 1:
					self.__dict__[s+"_exp"] -= 2 * self.__dict__["base_"+s] + 1
					self.__dict__["base_"+s] += 1
					if not s in d2:
						d2.append(s)
			self.save()
			self.update_vars(d2)
			return d
		elif isinstance(d, int):
			if stat:
				return self.add_experience({stat:d})
			else:
				from main.utils import distribute
				weights = [1,3,2,2,1,1]
				exp = distribute(d, weights)
				s = ['brawn','charm','finesse','lore','magery','stamina']
				stats = dict(zip(s,exp))
				return self.add_experience(stats)
		else:
			return None

	def new_pvm_combat(self, enemy):
		self.combat_messages = [[]]
		self.save()
		return super(Hero,self).new_pvm_combat(enemy, self.destination)

	def __unicode__(self):
		return self.name + " " + self.family_name
