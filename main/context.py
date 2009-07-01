# -*- coding: utf-8 -*-
from models import Hero

def hero(request):
	if (request.user.is_authenticated()):
		hero = Hero.objects.get(user=request.user)
		return {'hero':hero}
	return {}
