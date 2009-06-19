# -*- coding: utf-8 -*-
from django.contrib import admin
from dp.main.models import Enemy, CombatMessage, Item
#from django.contrib.sessions import session

class EnemyAdmin(admin.ModelAdmin):
	list_display = ('name', 'json_variety', 'count', 'gender')

class CombatMessageAdmin(admin.ModelAdmin):
	list_display = ('action', 'message')

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name',)

admin.site.register(Enemy, EnemyAdmin)
admin.site.register(CombatMessage, CombatMessageAdmin)
admin.site.register(Item, ItemAdmin)
