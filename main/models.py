# -*- coding: utf-8 -*-
from django.db import models
from django.template import Context,Template
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save

import random
from JSONField import JSONField

# Create your models here.

class Skill(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Enemy(models.Model):
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

	def new_combatant(self):
		c = Combatant(enemy=self, brawn=self.base_brawn,
			charm=self.base_charm, finesse=self.base_finesse,
			lore=self.base_lore, magery=self.base_magery,
			stamina=self.base_stamina)
		c.save()
		return c

	def __unicode__(self):
		return self.name

class Item(models.Model):
	name = models.CharField(max_length=50)
	article = models.CharField(max_length=20)
	multiplename = models.CharField(max_length=50)
	image_url = models.URLField()
	variety = JSONField()
	def __unicode__(self):
		return self.name

class Hero(models.Model):
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
	location = models.ForeignKey('Location', default='tree_village')

	inventory = models.ManyToManyField(Item, through='InventoryItem')

	combatant = models.ForeignKey('Combatant', db_index=True, blank=True, null=True)

	def new_pvm_combat(self, enemy):
		c = Combat(location=random.choice(Location.objects.all()), challenger=self.combatant, opposition=enemy.new_combatant())
		return c

	def _new_combatant(self):
		if (not self.combatant):
			c = Combatant(enemy=None, brawn=self.base_brawn,
				charm=self.base_charm, finesse=self.base_finesse,
				lore=self.base_lore, magery=self.base_magery,
				stamina=self.base_stamina)
			c.save()
			self.combatant = c;

	def __unicode__(self):
		return self.name + " " + self.family_name
def make_hero_combatant(sender, instance, **kwargs):
	instance._new_combatant()
pre_save.connect(make_hero_combatant, sender=Hero)

class Effect(models.Model):
	name = models.CharField(max_length=50)

class Combatant(models.Model):
	enemy = models.ForeignKey(Enemy, null=True, blank=True, db_index=True)

	brawn = models.IntegerField()
	charm = models.IntegerField()
	finesse = models.IntegerField()
	lore = models.IntegerField()
	magery = models.IntegerField()
	stamina = models.IntegerField()

	effects = models.ManyToManyField(Effect, through='EffectInstance')
	skills = models.ManyToManyField(Skill)

	def _get_hero(self):
		return Hero.objects.filter(combatant=self)[0]
	hero = property(_get_hero)

	def __unicode__(self):
		return (self.hero or self.enemy).__unicode__()

class EffectInstance(models.Model):
	effect = models.ForeignKey(Effect)
	target = models.ForeignKey(Combatant)
	duration = models.IntegerField()
	unit = models.CharField(max_length=1, choices=(
		('a','Attack'),('c','Combat'),('d','Day'),('v','Adventure'),('r','Round of Combat')))


class Message(models.Model):
	"""
	>>> message = Message.objects.create(message='Test {{en.name}} h{{en.count|pluralize:"i,ello"}} {{loc.tool|random}}')
	>>> enemy = Enemy.objects.create(name='fred', count=1)
	>>> loc = Location.objects.create(tool='["barbell"]')
	>>> message.transmogrify({'en':enemy,'loc':loc})
	u'Test fred hi barbell'
	"""
	action = models.CharField(max_length=50, db_index=True)
	message = models.TextField()

	def transmogrify(self, a):
		t = Template(self.message)
		c = Context(a)
		return t.render(c)

class Item(models.Model):
	name = models.CharField(max_length=50)
	article = models.CharField(max_length=20)
	multiplename = models.CharField(max_length=50)
	image_url = models.URLField()
	variety = JSONField()
	def __unicode__(self):
		return self.name

class Encounter(models.Model):
	name = models.CharField(max_length=50, null=True, blank=True)
	description = models.CharField(max_length=100)
	combatible = models.BooleanField()
	enemy = models.ForeignKey(Enemy, null=True, blank=True)
	def __unicode__(self):
		return self.name or ("Battle of " + self.enemy.name)

class Location(models.Model):
	name = models.CharField(max_length=50)
	enemies = models.ManyToManyField(Enemy, blank=True)
	neighbors = models.ManyToManyField("self", blank=True)
	encounters = models.ManyToManyField(Encounter, blank=True, through="EncounterInfo")
	slug = models.CharField(max_length=50, primary_key=True)
	platform = JSONField()
	floor = JSONField()
	wall = JSONField()
	tool = JSONField()
	hole = JSONField()

	def __unicode__(self):
		return self.name

class Combat:
	def __init__(self, location, challenger, opposition):
		self.challenger = challenger
		self.opposition = opposition
		self.turn = 0
		self.done = False
		self.location = location
		self.next_round()

	def win(self):
		winitems = {}
		winitems[random.choice(Item.objects.all())] = 1
		while random.choice([True,False]):
			item = random.choice(Item.objects.all())
			if not item in winitems:
				winitems[item] = 1
			else:
				winitems[item] += 1
		for key,value in winitems.iteritems():
			InventoryItem.add_item(self.challenger.hero,key,value)
		self.done = True
		self.winitems = winitems
		self.result = 'won'

	def won(self):
		return self.result == 'won'

	def lose(self):
		self.done = True
		self.result = 'lost'

	def next_round(self):
		self.turn += 1
		who_message = random.choice(Message.objects.filter(action='who'))
		self.messages = [who_message.transmogrify({'en':self.opposition.enemy, 'loc':self.location})]

	def addmessage(self, action):
		message = random.choice(Message.objects.filter(action=action))
		self.messages.append(message.transmogrify({'en':self.opposition.enemy, 'loc':self.location}))

	def challenger_hit(self): self.addmessage('you hit')
	def challenger_miss(self): self.addmessage('you miss')
	def opposition_hit(self): self.addmessage('enemy hits')
	def opposition_miss(self): self.addmessage('enemy misses')

class InventoryItem(models.Model):
	owner = models.ForeignKey(Hero, db_index=True)
	item = models.ForeignKey(Item)
	quantity = models.IntegerField()

	def add_item(cls, owner, item, quantity=1):
		try:
			prior = cls.objects.get(owner=owner, item=item)
			prior.quantity += quantity
			prior.save()
		except ObjectDoesNotExist:
			cls(owner=owner, item=item, quantity=quantity).save()
	add_item=classmethod(add_item)

class EncounterInfo(models.Model):
	encounterrate = models.IntegerField()
	location = models.ForeignKey(Location)
	encounter = models.ForeignKey(Encounter)
