#! /usr/bin/env python3

import numpy as np
import pickle
import random
import os
import operator
from copy import deepcopy


NRPOPS = 25

def main():
	# initialisation	
	
	w = 0.7298
	generations = 200
	v0 = np.zeros([NRPOPS,5,300, 300])
	per_best_fitness = np.zeros(NRPOPS)
	population = []
	for model in range(NRPOPS-1):
    		population.append(pickle.load(open("current_best_run.p", "rb")))
		
	newpopulation = mutate(population, 0.5, 1)
	newpopulation.append(pickle.load(open("current_best_run.p", "rb")))
	population = deepcopy(newpopulation)
	per_best_model = deepcopy(newpopulation)
	
	
	for times in range(generations):
		
		print('Generation', times)
		#w -= 0.02
		fitness, per_best_fitness, per_best_model = test(population, per_best_fitness, per_best_model)
		ind = []
		ind = np.argsort(fitness)
		print(ind[-1])
		glob_best_model = deepcopy(population[ind[-1]])
		pickle.dump(model, open("Swarm_Global_Best_model.p","wb"))	
		newpop, v = adjust(population, glob_best_model, per_best_model, w, v0)
		v0 = deepcopy(v)
		population = deepcopy(newpop)


def test(population, per_best_fitness, per_best_model):
	fitness = np.zeros(NRPOPS)
	fit1 = 0
	fit2 = 0
	for i, model in enumerate(population):
		print('Model run', i)
		pickle.dump(model, open("currentmodel.p","wb"))	
		os.system("./loop.py")
		fit1 = pickle.load(open("fitness.p", "rb"))
		#os.system("./loop.py")
		#fit2 = pickle.load(open("fitness.p", "rb"))
		fitness[i]= (fit1+fit2)
		if fitness[i] > per_best_fitness[i]:
			per_best_fitness[i] = fitness[i]
			per_best_model[i] = model
	print(fitness)
	return fitness, per_best_fitness, per_best_model

def adjust(pop, glob_best_model, per_best_model, w, v0):
	v1 = np.zeros([NRPOPS,5,300, 300])
	for i, model in enumerate(pop):
		for j, layer in enumerate(model.coefs_):
			for k, node in enumerate(layer):
				for l, weight in enumerate(node):
					v1[i][j][k][l] = w * v0[i][j][k][l] + random.uniform(0, 1.49618)*(per_best_model[i].coefs_[j][k][l]-pop[i].coefs_[j][k][l]) + random.uniform(0, 1.49618)*(glob_best_model.coefs_[j][k][l]-pop[i].coefs_[j][k][l])
					pop[i].coefs_[j][k][l] += v1[i][j][k][l]
	v = deepcopy(v1)
	return pop, v



def mutate(pop, rate, div):
	for i, model in enumerate(pop):
		for j, layer in enumerate(model.coefs_):
			for k, node in enumerate(layer):
				for l, weight in enumerate(node):
					if random.uniform(0, 1) <= rate:
						pop[i].coefs_[j][k][l] += div*(0.5 - np.random.random(1))

	return pop




if __name__ == '__main__':
	main()
