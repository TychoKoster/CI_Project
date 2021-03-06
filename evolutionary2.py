#! /usr/bin/env python3

import numpy as np
import pickle
import random
import os
import operator
from copy import deepcopy


def main():
	# initialisation	
	nrpops = 16
	maxfit = 0
	population = []
	newpopulation1 = []
	evolved_max_fitness = []
	
	evolved_fitness = []
	for model in range(nrpops-1):
		fi = open('current_best_run.p', 'rb')
		population.append(pickle.load(fi))
		fi.close()

	# First one is not mutated	
	newpopulation = mutate(population, 1, 0.01)
	fi = open('current_best_run.p', 'rb')
	newpopulation1.append(pickle.load(fi))
	fi.close()
	for model in range(len(newpopulation)):
		newpopulation1.append(newpopulation[model])
	population = deepcopy(newpopulation1)
	generations = 100
	
	for times in range(generations):
		
		print('Generation', times)
		
		# Race and determine fitness		
		fitness, maxfit, improvement = test(population, maxfit)
		evolved_max_fitness.append(maxfit)
		evolved_fitness.append(np.amax(fitness))
		fi = open("evolved_max_fitness.p","wb")
		pickle.dump(evolved_max_fitness, fi)
		fi.close()
		fi = open("evolved_fitness.p","wb")
		pickle.dump(evolved_fitness, fi)
		fi.close()

		# Tournament selection for selecting best genotypes.
		ind = []
		ind = np.argsort(fitness)
		print(ind[-1])
		print(ind[-2])
		if improvement:
			bestpop = deepcopy(population[ind[-1]])
			secondbest = deepcopy(population[ind[-2]])
			thirdbest = deepcopy(population[ind[-3]])
			bestrun = deepcopy(bestpop)
			secondrun = deepcopy(secondbest)
			thirdrun = deepcopy(thirdbest)
			fit1 = fitness[ind[-1]]
			fit2 = fitness[ind[-2]]
			fit3 = fitness[ind[-3]]
			fi = open("current_best_run.p","wb")
			pickle.dump(bestpop, fi)
			fi.close()
			fi = open("current_secondbest_run.p","wb")
			pickle.dump(secondbest, fi)
			fi.close()
			fi = open("current_thirdbest_run.p","wb")
			pickle.dump(thirdbest, fi)
			fi.close()
		else:
			secondbest = deepcopy(population[ind[-1]])
			thirdbest = deepcopy(population[ind[-2]])
			secondrun = deepcopy(secondbest)
			thirdrun = deepcopy(thirdbest)
			fit2 = fitness[ind[-1]]
			fit3 = fitness[ind[-2]]
			fi = open("current_secondbest_run.p","wb")
			pickle.dump(secondbest, fi)
			fi.close()
			fi = open("current_thirdbest_run.p","wb")
			pickle.dump(thirdbest, fi)
			fi.close()
	
		# Make new population out of nr. 1, 2 and 3.	
		population = []
		population.append(thirdbest)
		fit_total = fit1 + fit2 + fit3
		for model in range(11):
			# Fitness Propotional
			
			portion = random.uniform(0,1)
			if portion < (fit1/fit_total):
				fi = open("current_best_run.p","rb")
				population.append(pickle.load(fi))
				fi.close()
			elif portion < (fit1+fit2)/(fit_total):
				fi = open("current_secondbest_run.p", "rb")
				population.append(pickle.load(fi))
				fi.close()
			else:
				fi = open("current_thirdbest_run.p", "rb")
				population.append(pickle.load(fi))
				fi.close()
		
		# Mutation, rate of mutations is declining with generations.
		newpop = mutate(population, 0.01*float(generations/(times+1)), 0.0001*float(generations/(times+1)))
		newpop1 = deepcopy(newpop)
		

		# Crossover: Breeding of kids, from best 2 genotypes
		kid1, kid2, kid3, kid4 = crossover(bestrun, secondrun)
		newpop1.append(kid1)
		newpop1.append(kid2)
		newpop1.append(kid3)
		newpop1.append(kid4)
		population = deepcopy(newpop1)
	

def test(population, maxfit):
	fitness = np.zeros(16)
	fit1 = 0
	fit2 = 0
	fit3 = 0
	improvement = False
	for i, model in enumerate(population):
		print('Model run', i)

		# Three runs to prevent stochasticity
		fi = open("currentmodel.p","wb")
		pickle.dump(model, fi)	
		fi.close()
		os.system("./loop.py")
		fi = open("fitness.p", "rb")
		fit1 = pickle.load(fi)
		fi.close()
		fitness[i]= (fit1+fit2+fit3)
		
		#pickle.dump(model, open("currentmodel.p","wb"))	
		#os.system("./loop.py")
		#fit2 = pickle.load(open("fitness.p", "rb"))
		#pickle.dump(model, open("currentmodel.p","wb"))	
		#os.system("./loop.py")
		#fit3 = pickle.load(open("fitness.p", "rb"))
		if fitness[i] > 199:
			break
	print(fitness)
	maxfitness = np.amax(fitness)
	if maxfitness > maxfit:
		maxfit = maxfitness
		improvement = True
	print(maxfit, improvement)
	if maxfit > 199:
		maxfit = 0
	return fitness, maxfit, improvement
		



def mutate(pop, rate, div):
	for i, model in enumerate(pop):
		for j, layer in enumerate(model.coefs_):
			for k, node in enumerate(layer):
				for l, weight in enumerate(node):
					if random.uniform(0, 1) <= rate:
						pop[i].coefs_[j][k][l] += div*(0.5 - np.random.random(1))

	return pop


def crossover(gen1,gen2):
	# Create next generation out of best two genotypes
	kid1, kid2 = two_point_crossover(gen1, gen2)
	kid3, kid4 = single_point_crossover(gen1, gen2)
	
	return kid1, kid2, kid3, kid4

def single_point_crossover(model_1, model_2):
	weights_1 = model_1.coefs_
	layer_index = random.randint(0, len(weights_1) - 1)

	crossover_point = random.randint(0, len(weights_1[layer_index]) - 1)

	model_1_slice = model_1.coefs_[layer_index][crossover_point:]
	model_2_slice = model_2.coefs_[layer_index][crossover_point:]

	model_1.coefs_[layer_index][crossover_point:] = model_2_slice
	model_2.coefs_[layer_index][crossover_point:] = model_1_slice

	return model_1, model_2

def two_point_crossover(model_1, model_2):
	weights_1 = model_1.coefs_
	layer_index = random.randint(0, len(weights_1) - 1)

	crossover_point_1 = random.randint(0, len(weights_1[layer_index]) - 2)
	crossover_point_2 = random.randint(crossover_point_1, len(weights_1[layer_index]) - 1)

	model_1_slice = model_1.coefs_[layer_index][crossover_point_1:crossover_point_2]
	model_2_slice = model_2.coefs_[layer_index][crossover_point_1:crossover_point_2]

	model_1.coefs_[layer_index][crossover_point_1:crossover_point_2] = model_2_slice
	model_2.coefs_[layer_index][crossover_point_1:crossover_point_2] = model_1_slice

	return model_1, model_2


if __name__ == '__main__':
	main()
