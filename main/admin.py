# -*- coding: utf-8 -*-
from django.contrib import admin
from dp.main.models import Enemy, Message, Item, Location, InventoryItem, Hero, Combatant, Effect, EffectInstance
#from django.contrib.sessions import session

class EnemyAdmin(admin.ModelAdmin):
	list_display = ('name', 'variety', 'count', 'gender')

class MessageAdmin(admin.ModelAdmin):
	list_display = ('action', 'message')

class LocationAdmin(admin.ModelAdmin):
	list_display = ('name', 'parent')

class HeroAdmin(admin.ModelAdmin):
	list_display = ('name', 'family_name', 'user', 'gender', 'variety')

class InventoryAdmin(admin.ModelAdmin):
	list_display = ('owner', 'item', 'quantity')

class CombatantAdmin(admin.ModelAdmin):
	list_display = ('hero', 'enemy')

class EffectAdmin(admin.ModelAdmin):
	list_display = ('name')

class EffectInstance(admin.ModelAdmin):
	list_displat = ('target', 'effect', 'duration', 'unit')

#admin.site.register(Enemy, EnemyAdmin)
#admin.site.register(Message, MessageAdmin)
#admin.site.register(Item)
#admin.site.register(Location, LocationAdmin)
#admin.site.register(InventoryItem, InventoryAdmin)
#admin.site.register(Hero, HeroAdmin)
#admin.site.register(Combatant, CombatantAdmin)
admin.site.register(Effect, EffectAdmin)
admin.site.register(EffectInstance, EffectInstanceAdmin)