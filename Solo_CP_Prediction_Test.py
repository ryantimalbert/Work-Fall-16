import cPickle as pickle
from sklearn import svm, cross_validation, preprocessing
import sys
import time
from sklearn.ensemble import RandomForestClassifier
import csv
import numpy
# database_file = open('TestingDBs.txt', 'r')
# genomes = database_file.readlines()
# function_results = {}
# for genome in genomes:
# 	genome = genome.replace('\n', '')
# 	file = open('2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = genome), 'rb')
# 	data_Arrays = pickle.load(file)
# 	training_vector = []
# 	target_vector = []
# 	for i in range(len(data_Arrays[0])):
# 		if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
# 			pass
# 		elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
# 			pass
# 		else:
# 			training_vector.append(data_Arrays[0][i])
# 			target_vector.append(data_Arrays[1][i])
# 	training_vector1 = []
# 	for i in training_vector:
# 		training_vector1.append([i[2]])
# 	data1 = open('data/{database}.txt'.format(database = genome), 'r')
# 	file.close()
# 	data = pickle.load(data1)
# 	data1.close()
# 	data = data[0]
# 	function_results[genome] = []
# 	function_results[genome].append(data)
# 	clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
# 	score = cross_validation.cross_val_score(clf, training_vector1, target_vector, cv = 5)
# 	function_results[genome].append(score.mean())

# save_file = open('Compare_CP', 'wb')
# serial = pickle.dumps(function_results)
# save_file.write(serial)
# save_file.close()
file = open('Compare_CP', 'r')
function_results = pickle.load(file)
file.close()
Composite_data = []
CP_data = []
for genome in function_results:
	data = function_results[genome]
	Composite_data.append(data[0])
	CP_data.append(data[1])
print(numpy.mean(Composite_data))
print(numpy.std(Composite_data))
print(numpy.mean(CP_data))
print(numpy.std(CP_data))
# file = open('Scatter_CP_VS_Function.csv', 'wb')
# writer = csv.writer(file, quoting=csv.QUOTE_ALL)
# for name in function_results:
# 	internal_array = []
# 	data_array = function_results[name]
# 	print(name)
# 	print(data_array[0])
# 	print(data_array[1])
# 	internal_array.append(name)
# 	internal_array.append(data_array[0] * 100)
# 	internal_array.append(data_array[1] * 100)
# 	writer.writerow(internal_array)
# file.close()