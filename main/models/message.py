# -*- coding: utf-8 -*-
from django.db import models
from django.template import Context,Template

class Message(models.Model):
	class Meta:
		app_label = 'main'
	"""
	>>> message = Message.objects.create(message='Test {{en.name}} h{{en.count|pluralize:"i,ello"}} {{loc.tool|random}}')
	>>> enemy = Enemy.objects.create(name='fred', count=1)
	>>> loc = Location.objects.create(tool='["barbell"]')
	>>> message.transmogrify({'en':enemy,'loc':loc})
	u'Test fred hi barbell'
	"""
	action = models.CharField(max_length=50, db_index=True)
	message = models.TextField()

	def transmogrify(self, a):
		t = Template(self.message)
		c = Context(a)
		return t.render(c)
