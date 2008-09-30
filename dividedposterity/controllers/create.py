from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
#from google.appengine.ext import db

from dividedposterity.models import Hero, Buff, Effect, PVMCombat
from dividedposterity.modelforms import HeroForm, EffectForm, BuffForm, PVMCombatForm

def route(request, model):
	form = {'hero': HeroForm,
	        'effect': EffectForm,
			'buff': BuffForm,
			'PVMCombat': PVMCombatForm
	       }[model](request.POST)
	if not form.is_valid():
		return render_to_response('fixform.djt',{'model':model,'form':form})
	form.save()
	return HttpResponseRedirect('/forms')
