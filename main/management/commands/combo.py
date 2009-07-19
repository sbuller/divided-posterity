# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.core.management import call_command

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		call_command('reset', 'main', noinput=True)
		call_command('syncdb', noinput=True)
		call_command('loaddata', 'items', 'messages', 'enemies', 'locations', 'heros', 'encounters', 'encounterinfos', 'skills', 'triggers', 'actions', 'combatantskills', 'effects')
