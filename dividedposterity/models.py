#from django.db import models
from appengine_django.models import BaseModel
from google.appengine.ext import db

# Create your models here.

class PVMCombat(BaseModel):
	player_hp_lost = db.IntegerProperty()
	player_mp_used = db.IntegerProperty()

	monster_hp_lost = db.IntegerProperty()
	monster_mp_used = db.IntegerProperty()

	# don't forget ID & duration
	effects = db.ListProperty(str)
	behaviour_data = db.StringProperty()

	turn = db.IntegerProperty()

class Hero(BaseModel):
	name = db.StringProperty(required=True)
	gender = db.StringProperty(choices=set(["male","female"]))
	id = db.IntegerProperty()

	brawn = db.IntegerProperty()
	lore = db.IntegerProperty()
	stamina = db.IntegerProperty()
	charm = db.IntegerProperty()
	magery = db.IntegerProperty()
	finesse = db.IntegerProperty()

	basebrawn = db.IntegerProperty()
	baselore = db.IntegerProperty()
	basestamina = db.IntegerProperty()
	basecharm = db.IntegerProperty()
	basemagery = db.IntegerProperty()
	basefinesse = db.IntegerProperty()

	hp = db.IntegerProperty()
	mp = db.IntegerProperty()

	# f(x) = mx + b
	resists_m = db.ListProperty(float,default=[])
	resists_b = db.ListProperty(int,default=[])

	adventure_total = db.IntegerProperty()
	adventure = db.IntegerProperty()

	cclass = db.StringProperty(choices=set(["Book Crook","Shape Shifter","Eagle Archer","Dune Watcher","Bricksmith","Jade Shaman"]))

	combat = db.ReferenceProperty(PVMCombat)


class Buff(BaseModel):
	target = db.ReferenceProperty(Hero,collection_name='target_set')
	source = db.ReferenceProperty(Hero,collection_name='source_set')
	sourcename = db.StringProperty()
	buffname = db.StringProperty()

class Effect(BaseModel):
	effectname = db.StringProperty()
	target = db.ReferenceProperty(Hero)
	quantity = db.IntegerProperty()
	unit = db.StringProperty(choices=set(["adventure","combat","day","turn"]))
	order = db.IntegerProperty()

class Monster(BaseModel):
	brawn = db.IntegerProperty()
	lore = db.IntegerProperty()
	stamina = db.IntegerProperty()
	charm = db.IntegerProperty()
	magery = db.IntegerProperty()
	finesse = db.IntegerProperty()

	hp = db.IntegerProperty()
	mp = db.IntegerProperty()

	# f(x) = mx + b
	resists_m = db.ListProperty(float)
	resists_b = db.ListProperty(int)

	# victory & loss conditions, Combat Strategies, Initiative Script
	behaviour = db.IntegerProperty()

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