# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from models import Message, Enemy, Item, Location, Combat, InventoryItem, Hero

import random, json

def index(request):
	if request.user.is_authenticated():
		hero = Hero.objects.get(user=request.user)
		return render_to_response('main/main.djt', {'hero':hero,'user':request.user})
	else:
		return render_to_response('main/index.djt')

@login_required
def startcombat(request):
	if not 'location' in request.session:
		request.session['location'] = random.choice(Location.objects.all())

	combat = Combat(request.session['location'], request.user)
	request.session['combat'] = combat

	return render_to_response('main/combat.djt',{'combat':combat})

@login_required
def combat(request):
	combat = request.session['combat']
	combat.next_round()

	if 'youhit' in request.POST:
		if request.POST['youhit'] == 'true':
			combat.youhit()
		else:
			combat.youmiss()
	if 'theyhit' in request.POST:
		if request.POST['theyhit'] == 'true':
			combat.theyhit()
		else:
			combat.theymiss()

	if 'win' in request.POST:
		combat.win()
	elif 'lose' in request.POST:
		combat.lose()

	request.session['combat'] = combat
	if combat.done:
		return HttpResponseRedirect('/aftercombat')

	return render_to_response('main/combat.djt', {'combat': combat})

@login_required
def aftercombat(request):
	return render_to_response('main/aftercombat.djt', {'combat': request.session['combat']})

@login_required
def inventory(request):
	owner = Hero.objects.get(user=request.user)
	inventory = InventoryItem.objects.filter(owner=owner)
	return render_to_response('main/inventory.djt', {'items':inventory})

@login_required
def locationMap(request, location_id='root'):
	places = {}
	location = Location.objects.get(slug=location_id)
	for it in location.neighbors.all():
		places[it.slug] = it
		print it
	print places
	request.session['location'] = location
	return render_to_response("main/maps/"+location.slug+".djt", {'location':location,'places':places})
