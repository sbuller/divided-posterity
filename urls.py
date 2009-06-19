# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('dp.main.views',
	(r'^$', 'index'),
	(r'^combat', 'combat'),
	(r'^startcombat', 'startcombat'),
	(r'^aftercombat', 'aftercombat'),
	# Example:
	# (r'^dp/', include('dp.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs'
	# to INSTALLED_APPS to enable admin documentation:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/(.*)', admin.site.root),
)
