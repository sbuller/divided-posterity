# -*- coding: utf-8 -*-
from django.contrib import admin
from dp.main.models import Enemy, CombatMessage
#from django.contrib.sessions import session

class EnemyAdmin(admin.ModelAdmin):
	list_display = ('name', 'json_variety', 'count', 'gender')

class CombatMessageAdmin(admin.ModelAdmin):
	list_display = ('action', 'message')

admin.site.register(Enemy, EnemyAdmin)
admin.site.register(CombatMessage, CombatMessageAdmin)