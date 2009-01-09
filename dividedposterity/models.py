from django.db import models

# Create your models here.

class PVMCombat(models.Model):
	player_hp_lost = models.IntegerField()
	player_mp_used = models.IntegerField()

	monster_hp_lost = models.IntegerField()
	monster_mp_used = models.IntegerField()

	# don't forget ID & duration
	effects = db.ListProperty(str)
	behaviour_data = db.StringProperty()

	turn = models.IntegerField()

class Hero(models.Model):
	name = db.StringProperty(required=True)
	gender = db.StringProperty(choices=set(["male","female"]))
	id = models.IntegerField()

	brawn = models.IntegerField()
	lore = models.IntegerField()
	stamina = models.IntegerField()
	charm = models.IntegerField()
	magery = models.IntegerField()
	finesse = models.IntegerField()

	basebrawn = models.IntegerField()
	baselore = models.IntegerField()
	basestamina = models.IntegerField()
	basecharm = models.IntegerField()
	basemagery = models.IntegerField()
	basefinesse = models.IntegerField()

	hp = models.IntegerField()
	mp = models.IntegerField()

	# f(x) = mx + b
	resists_m = db.ListProperty(float,default=[])
	resists_b = db.ListProperty(int,default=[])

	adventure_total = models.IntegerField()
	adventure = models.IntegerField()

	cclass = db.StringProperty(choices=set(["Book Crook","Shape Shifter","Eagle Archer","Dune Watcher","Bricksmith","Jade Shaman"]))

	combat = db.ReferenceProperty(PVMCombat)


class Buff(models.Model):
	target = db.ReferenceProperty(Hero,collection_name='target_set')
	source = db.ReferenceProperty(Hero,collection_name='source_set')
	sourcename = db.StringProperty()
	buffname = db.StringProperty()

class Effect(models.Model):
	effectname = db.StringProperty()
	target = db.ReferenceProperty(Hero)
	quantity = models.IntegerField()
	unit = db.StringProperty(choices=set(["adventure","combat","day","turn"]))
	order = models.IntegerField()

class Monster(models.Model):
	brawn = models.IntegerField()
	lore = models.IntegerField()
	stamina = models.IntegerField()
	charm = models.IntegerField()
	magery = models.IntegerField()
	finesse = models.IntegerField()

	hp = models.IntegerField()
	mp = models.IntegerField()

	# f(x) = mx + b
	resists_m = db.ListProperty(float)
	resists_b = db.ListProperty(int)

	# victory & loss conditions, Combat Strategies, Initiative Script
	behaviour = models.IntegerField()

###############################################################################
# Convenience functions requiring multiple model definitions                  #
###############################################################################

def herodisplay(self):
	def change(value,base):
		return "increased" if value>base else "decreased" if value<base else "uncreased"
	buffs = Buff.all().filter('target = ', self).order('sourcename').order('buffname').fetch(100)
	effects = Effect.all().filter('target = ', self).order('order').order('quantity').fetch(100)
	return {
		'hero':self,
		'buffs':buffs,
		'effects':effects,
		'stats':[
			{'stat':"Brawn", 'base':self.basebrawn, 'value':self.brawn, 'change':change(self.brawn,self.basebrawn)},
			{'stat':"Magery", 'base':self.basemagery, 'value':self.magery, 'change':change(self.magery,self.basemagery)},
			{'stat':"Stamina", 'base':self.basestamina, 'value':self.stamina, 'change':change(self.stamina,self.basestamina)},
			{'stat':"Finesse", 'base':self.basefinesse, 'value':self.finesse, 'change':change(self.finesse,self.basefinesse)},
			{'stat':"Charm", 'base':self.basecharm, 'value':self.charm, 'change':change(self.charm,self.basecharm)},
			{'stat':"Lore", 'base':self.baselore, 'value':self.lore, 'change':change(self.lore,self.baselore)}
		]
	}
Hero._display = herodisplay
