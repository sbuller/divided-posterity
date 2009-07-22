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

	combat_messages = JSONField()

	non_combat = models.ForeignKey('NonCombat', null=True, blank=True)

	#equipped_items = models.ManyToManyField('Item',through='EquippedItem')

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

	def add_experience(self, d, stat=None):
		if isinstance(d, dict):
			print d
			d2 = []
			for s, amt in d.items():
				self.__dict__[s+"_exp"] += amt
				while self.__dict__[s+"_exp"] > 2 * self.__dict__["base_"+s] + 1:
					self.__dict__[s+"_exp"] -= 2 * self.__dict__["base_"+s] + 1
					self.__dict__["base_"+s] += 1
					if not s in d2:
						d2.append(s)
			self.save()
			self.update_vars(d2)
		elif isinstance(d, int):
			if stat:
				self.add_experience({stat:d})
			else:
				import random
				rnums = [0] + map(random.randint, [0]*5, [d+4]*5) + [d+4]
				rnums.sort()
				s = ['brawn','charm','finesse','lore','magery','stamina']
				stats = {}
				for i in xrange(6):
					stats[s[i]] = rnums[i+1]-rnums[i]
				self.add_experience(stats)

	def new_pvm_combat(self, enemy):
		self.combat_messages = [[]]
		self.save()
		return super(Hero,self).new_pvm_combat(enemy, self.destination)

	def __unicode__(self):
		return self.name + " " + self.family_name
