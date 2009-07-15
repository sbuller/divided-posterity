# -*- coding: utf-8 -*-
from django.db import models

from JSONField import JSONField

from combatant import Combatant
from skill import Skill

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

	base_brawn = models.IntegerField()
	base_charm = models.IntegerField()
	base_finesse = models.IntegerField()
	base_lore = models.IntegerField()
	base_magery = models.IntegerField()
	base_stamina = models.IntegerField()

	t_skills = models.ManyToManyField(Skill)

	def perform_action(self, combatant, combat):
		import random
		from combatantskill import CombatantSkill
		skill = random.choice(combatant.skills.all())
		target = random.choice(Combatant.objects.filter(combat=combat).exclude(team=combatant.team))
		cskill = CombatantSkill.objects.filter(combatant=combatant, skill=skill)[0]
		skill.invoke(actor=combatant, target=target, cskill=cskill, combat=combat)

	def new_combatant(self, combat):
		def add_skill_to_combatant(skill, combatant):
			from combatantskill import CombatantSkill
			CombatantSkill(skill = skill, mastery_level=1, combatant=combatant).save()

		c = Combatant(enemy=self, brawn=self.base_brawn,
			charm=self.base_charm, finesse=self.base_finesse,
			lore=self.base_lore, magery=self.base_magery,
			stamina=self.base_stamina, combat=combat,
			gender=self.gender, count=self.count)
		c.save()
		for skill in self.t_skills.all():
			add_skill_to_combatant(skill, c)
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
