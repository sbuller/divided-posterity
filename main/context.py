# -*- coding: utf-8 -*-
from models import Hero

def hero(request):
	hero = Hero.objects.get(user=request.user)
	return {'hero':hero}
