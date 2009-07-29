# -*- coding: utf-8 -*-
def distribute(total, weights):
	from numpy import random
	remainder = total
	total_weight = float(sum(weights))
	prob_left = 1.0
	a = []

	probs = [elem/total_weight for elem in weights][:-1]
	for it in probs:
		e = random.binomial(remainder, it/prob_left)
		a.append(e)
		remainder -= e
		prob_left -= it
	a.append(remainder)
	return a