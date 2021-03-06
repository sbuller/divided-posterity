# -*- coding: utf-8 -*-
from django.db import models
from django.template import Context,Template

class Message(models.Model):
	"""
	>>> message = Message.objects.create(message='Test {{en.name}} h{{en.count|pluralize:"i,ello"}} {{loc.tool|random}}')
	>>> enemy = Enemy.objects.create(name='fred', count=1)
	>>> loc = Location.objects.create(tool='["barbell"]')
	>>> message.transmogrify({'en':enemy,'loc':loc})
	u'Test fred hi barbell'
	"""
	class Meta:
		app_label = 'main'
	action = models.CharField(max_length=50, db_index=True)
	message = models.TextField()

	def transmogrify(self, a, pov=None):
		t = Template("{% load dp_extras %}" + self.message)
		if a['actor'].id == pov.id:
			a['actor'].player_pov = True
		if a['target'].id == pov.id:
			a['target'].player_pov = True
		c = Context(a)
		return t.render(c)
