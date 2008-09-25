from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
#from google.appengine.ext import db
from google.appengine.ext.db import djangoforms

from dividedposterity.models import Hero, Buff, Effect, PVMCombat
# Create your views here.

class HeroForm(djangoforms.ModelForm):
	class Meta:
		model = Hero
		exclude = ['resists_m','resists_b','adventure_total','adventure']

class EffectForm(djangoforms.ModelForm):
	class Meta:
		model = Effect

class BuffForm(djangoforms.ModelForm):
	class Meta:
		model = Buff

class PVMCombatForm(djangoforms.ModelForm):
	class Meta:
		model = PVMCombat

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