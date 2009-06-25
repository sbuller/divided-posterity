# -*- coding: utf-8 -*-
from django.db import models
from django.template import Context,Template
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

import random
from JSONField import JSONField

# Create your models here.

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

class Hero(models.Model):
	name = models.CharField(max_length=50)
	variety = models.CharField(max_length=50)
	family_name = models.CharField(max_length=50)
	gender = models.CharField(max_length=1, choices=(('m','Male'),('f','Female')))
	user = models.ForeignKey(User, db_index=True)

	brawn = models.IntegerField()
	charm = models.IntegerField()
	finesse = models.IntegerField()
	lore = models.IntegerField()
	magery = models.IntegerField()
	stamina = models.IntegerField()

	def __unicode__(self):
		return self.name + " " + self.family_name

class CombatMessage(models.Model):
	"""
	>>> message = CombatMessage.objects.create(message='Test {{en.name}} h{{en.count|pluralize:"i,ello"}} {{loc.tool|random}}')
	>>> enemy = Enemy.objects.create(name='fred', count=1)
	>>> loc = Location.objects.create(tool='["barbell"]')
	>>> message.transmogrify(enemy,loc)
	u'Test fred hi barbell'
	"""
	action = models.CharField(max_length=50, db_index=True)
	message = models.TextField()

	def transmogrify(self, enemy, location):
		t = Template(self.message)
		c = Context({'en':enemy, 'loc':location})
		return t.render(c)

class Item(models.Model):
	name = models.CharField(max_length=50)
	article = models.CharField(max_length=20)
	image_url = models.URLField()
	variety = JSONField()
	def __unicode__(self):
		return self.name

class Location(models.Model):
	name = models.CharField(max_length=50)
	parent = models.ForeignKey('self', null=True, blank=True, db_index=True)
	enemies = models.ManyToManyField(Enemy)
	platform = JSONField()
	floor = JSONField()
	wall = JSONField()
	tool = JSONField()
	hole = JSONField()

	def __unicode__(self):
		return self.name

class Combat:
	def __init__(self, location, user):
		self.hero = Hero.objects.get(user=user)
		self.enemy = random.choice(Enemy.objects.all())
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
			InventoryItem.add_item(self.hero,key,value)
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
		who_message = random.choice(CombatMessage.objects.filter(action='who'))
		self.messages = [who_message.transmogrify(self.enemy, self.location)]

	def addmessage(self, action):
		message = random.choice(CombatMessage.objects.filter(action=action))
		self.messages.append(message.transmogrify(self.enemy, self.location))

	def youhit(self): self.addmessage('you hit')
	def youmiss(self): self.addmessage('you miss')
	def theyhit(self): self.addmessage('enemy hits')
	def theymiss(self): self.addmessage('enemy misses')

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
