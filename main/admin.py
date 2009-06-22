# -*- coding: utf-8 -*-
from django.contrib import admin
from dp.main.models import Enemy, CombatMessage, Item, Location, InventoryItem
#from django.contrib.sessions import session

class EnemyAdmin(admin.ModelAdmin):
	list_display = ('name', 'variety', 'count', 'gender')

class CombatMessageAdmin(admin.ModelAdmin):
	list_display = ('action', 'message')

class LocationAdmin(admin.ModelAdmin):
	list_display = ('name', 'parent')

admin.site.register(Enemy, EnemyAdmin)
admin.site.register(CombatMessage, CombatMessageAdmin)
admin.site.register(Item)
admin.site.register(Location, LocationAdmin)
admin.site.register(InventoryItem)
