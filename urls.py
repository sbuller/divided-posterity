# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *
import settings

urlpatterns = patterns('dividedposterity.controllers', (r'^$', 'utility.defaultredirect'))

if settings.DEBUG:
	urlpatterns += patterns('dividedposterity.controllers',
		(r'^new(?P<model>.*)$', 'create.route')
	)

urlpatterns += patterns('dividedposterity.controllers',
		(r'^combat$', 'combat.route'),
		(r'^forms$', 'forms.route'),
		(r'^startcombat$', 'startcombat.route'),
		(r'^(?P<template>.*)$', 'utility.template')
    # Example:
    # (r'^foo/', include('foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)

if 0:
	urlpatterns += patterns('chat.views',
		(r'', '')
	)
