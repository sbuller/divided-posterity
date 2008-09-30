from google.appengine.ext.db import djangoforms
from dividedposterity.models import Hero, Buff, Effect, PVMCombat

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