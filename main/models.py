# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Enemy(models.Model):
	variety = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	em = models.CharField(max_length=10)
	ey = models.CharField(max_length=10)
	eir = models.CharField(max_length=10)
	emself = models.CharField(max_length=10)
	cEm = models.CharField(max_length=10)
	cEy = models.CharField(max_length=10)
	cEir = models.CharField(max_length=10)
	cEmself = models.CharField(max_length=10)
	plurality = models.BooleanField()

class CombatMessage(models.Model):
	action = models.CharField(max_length=50)
	message = models.TextField()
	words = models.TextField()