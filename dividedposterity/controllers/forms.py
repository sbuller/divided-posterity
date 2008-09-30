from django.shortcuts import render_to_response
from dividedposterity.modelforms import HeroForm,BuffForm,EffectForm,PVMCombatForm


def route(request):
	return render_to_response('forms.djt',{
		'heroform':HeroForm(),
		'buffform':BuffForm(),
		'effectform':EffectForm(),
		'pvmcombatform':PVMCombatForm()
		})
