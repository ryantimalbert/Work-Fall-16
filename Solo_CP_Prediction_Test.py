import cPickle as pickle
from sklearn import svm, cross_validation, preprocessing
import sys
import time
from sklearn.ensemble import RandomForestClassifier
database_file = open('TestingDBs.txt', 'r')
genomes = database_file.readlines()
function_results = {}
for genome in genomes:
	genome = genome.replace('\n', '')
	file = open('~/features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = genome), 'rb')
	data_Arrays = pickle.load(file)
	for i in range(len(data_Arrays[0])):
		if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
			pass
		elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
			pass
		else:
			training_vector.append(data_Arrays[0][i])
			target_vector.append(data_Arrays[1][i])
	training_vector1 = []
	for i in training_vector:
		training_vector1.append([i[2]])
		print(i[2])


# file = open('Scatter.csv', 'wb')
# 	writer = csv.writer(file, quoting=csv.QUOTE_ALL)
# 	array = []
# 	for name in data_readable:
# 		internal_array = []
# 		internal_array.append(name)
# 		point = data_readable[name][0]
# 		internal_array.append(point * 100)
# 		point = data_readable[name][1]
# 		internal_array.append(point * 100)
# 		point = data_readable[name][3]
# 		internal_array.append(point * 100)
# 		writer.writerow(internal_array)