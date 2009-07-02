# -*- coding: utf-8 -*-
from django.contrib import admin
from dp.main.models import Enemy, Message, Item, Location, InventoryItem, Hero, Combatant, Effect, EffectInstance, Encounter, EncounterInfo, Skill, Combat
#from django.contrib.sessions import session

class MessageAdmin(admin.ModelAdmin):
	list_display = ('id','action','message')

class LocationAdmin(admin.ModelAdmin):
	list_display = ('name',)

class InventoryAdmin(admin.ModelAdmin):
	list_display = ('id','owner','item','quantity')

class CombatantAdmin(admin.ModelAdmin):
	list_display = ('id','hero', 'enemy')

class HeroAdmin(admin.ModelAdmin):
	list_display = ('name','family_name','user','gender','variety')

class EnemyAdmin(admin.ModelAdmin):
	list_display = ('name','variety','count','gender')

class EffectAdmin(admin.ModelAdmin):
	list_display = ('name',)

class EffectInstanceAdmin(admin.ModelAdmin):
	list_display = ('id','target','effect','duration','unit')

class EncounterAdmin(admin.ModelAdmin):
	list_display=('name','description','combatible','enemy')

class EncounterInfoAdmin(admin.ModelAdmin):
	list_display=('id','encounter','location')

class CombatAdmin(admin.ModelAdmin):
	list_display=('id','challenger','opposition')

admin.site.register(Enemy, EnemyAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Item)
admin.site.register(Location, LocationAdmin)
admin.site.register(InventoryItem, InventoryAdmin)
admin.site.register(Hero, HeroAdmin)
admin.site.register(Combatant, CombatantAdmin)
admin.site.register(Effect, EffectAdmin)
admin.site.register(EffectInstance, EffectInstanceAdmin)
admin.site.register(Encounter, EncounterAdmin)
admin.site.register(EncounterInfo, EncounterInfoAdmin)
admin.site.register(Skill)
admin.site.register(Combat, CombatAdmin)
