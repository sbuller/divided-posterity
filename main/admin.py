# -*- coding: utf-8 -*-
from django.contrib import admin
from dp.main.models import Enemy, CombatMessage, Item, Location
#from django.contrib.sessions import session

class EnemyAdmin(admin.ModelAdmin):
	list_display = ('name', 'variety', 'count', 'gender')

class CombatMessageAdmin(admin.ModelAdmin):
	list_display = ('action', 'message')

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name',)
	
class LocationAdmin(admin.ModelAdmin):
	list_display = ('name', 'parent')

admin.site.register(Enemy, EnemyAdmin)
admin.site.register(CombatMessage, CombatMessageAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Location, LocationAdmin)
