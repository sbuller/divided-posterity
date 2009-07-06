# -*- coding: utf-8 -*-
from django.db import models

from JSONField import JSONField

from combatant import Combatant

class Enemy(models.Model):
	class Meta:
		app_label = 'main'
	"""
	>>> en = Enemy.objects.create(variety='["a","b","c"]',count=1)
	>>> " ".join(en.variety)
	u'a b c'
	"""
	variety = JSONField()
	name = models.CharField(max_length=50)
	count = models.IntegerField()
	gender = models.CharField(max_length=1, choices=(('m','Male'),('f','Female'),('n','Neutral'),('r','Randomly male or female')))

	def unspivak(self, x):
		table = [ #m,f,n,p
			['him','her','it','them'], #em
			['he','she','it','they'], #ey
			['his','her','its','their'], #eir
			['his','hers','its','theirs'], #eirs
			['himself','herself','itself','themselves'] #emself
		]
		gender = ['m','f','n','p']
		val = table[x][(3,gender.index(self.gender))[not self.count-1]]
		return val
	em = property(lambda s: s.unspivak(0))
	ey = property(lambda s: s.unspivak(1))
	eir = property(lambda s: s.unspivak(2))
	eirs = property(lambda s: s.unspivak(3))
	emself = property(lambda s: s.unspivak(4))

	base_brawn = models.IntegerField()
	base_charm = models.IntegerField()
	base_finesse = models.IntegerField()
	base_lore = models.IntegerField()
	base_magery = models.IntegerField()
	base_stamina = models.IntegerField()

	def new_combatant(self, combat):
		c = Combatant(enemy=self, brawn=self.base_brawn,
			charm=self.base_charm, finesse=self.base_finesse,
			lore=self.base_lore, magery=self.base_magery,
			stamina=self.base_stamina, combat=combat)
		c.save()
		return c

	def loot(self, combat, dropper):
		from item import Item,ItemDrop
		import random
		items = Item.objects.all()
		newitem = random.choice(items)
		ItemDrop.add_item(combat, dropper, newitem)
		while random.choice([True,False]):
			newitem = random.choice(items)
			ItemDrop.add_item(combat, dropper, newitem)

	def __unicode__(self):
		return self.name
