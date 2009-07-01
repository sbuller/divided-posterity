# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('dp.main.views',
	(r'^$', 'index'),
	(r'^combat$', 'combat'),
	(r'^startcombat$', 'startcombat'),
	(r'^aftercombat$', 'aftercombat'),
	(r'^inventory$', 'inventory'),
	(r'^map$', 'locationMap',{'location_id':''}),
	(r'^map/(?P<location_id>[\w\d]+)$', 'locationMap'),
	# Example:
	# (r'^dp/', include('dp.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs'
	# to INSTALLED_APPS to enable admin documentation:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/(.*)', admin.site.root),
)
urlpatterns += patterns('',
	(r'^login$', 'django.contrib.auth.views.login'),
	(r'^logout$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
	(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/images'}),
	(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/js'}),
	(r'^stylesheets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/stylesheets'}),
	(r'^favicon.ico$', 'django.views.static.serve', {'document_root': 'static/favicon.ico'}),

)
