# -*- coding: utf-8 -*-
from models import Hero

def hero(request):
	if (request.user.is_authenticated()):
		hero = Hero.objects.filter(user=request.user)[0]
		return {'hero':hero}
	return {}
