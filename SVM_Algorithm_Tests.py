import cPickle as pickle
from sklearn import svm, cross_validation, preprocessing
import sys
import time
from sklearn.ensemble import RandomForestClassifier
from features.Feature_Array_File_Parse import compile_feature_list
from features.DatabaseTrainingSetParsing import compile_feature_list_sb

def Cross_Validation_Test(Array):
	# unit_var_0_feature = Array[0]
	# min_max_feature = list(Array[0])
	# unit_var_0_feature = preprocessing.scale(unit_var_0_feature)

	# min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	# min_max_feature = min_max_scale.fit_transform(min_max_feature)
	# for i in range(0, 3):
	# 	for b in range(0, 3):
	# 		clf = svm.SVC(C = pow(1, i), gamma = pow(1, b))
	# 		clf2 = svm.SVC(C = pow(1, i), gamma = pow(1, b))
	# 		score1 = cross_validation.cross_val_score(clf, unit_var_0_feature, Array[1], cv = 5)
	# 		print(score1)
	# 		print('This is unit variance on gamma {gamma} and C {c}'.format(gamma = b, c = i))
	# 		score2 = cross_validation.cross_val_score(clf2, min_max_feature, Array[1], cv = 5)
	# 		print(score2)
	# 		print('This is min_max on gamma {gamma} and C {c}'.format(gamma = b, c = i))
	# without_ratio = list(Array[0])
	# for vector in without_ratio:
	# 	vector.pop(1)
	# unit_var_0_feature0_without = preprocessing.scale(without_ratio)
	# for i in range(-2, 2):
	# 	for b in range(-1, 1):
	# 		clf = svm.SVC(C = pow(1, i), gamma = pow(1, b))
	# 		clf2 = svm.SVC(C = pow(1, i), gamma = pow(1, b))
	# 		score1 = cross_validation.cross_val_score(clf, unit_var_0_feature, Array[1], cv = 5)
	# 		print(score1)
	# 		print(score1.mean())
	# 		print('This is unit variance on full feature gamma {gamma} and C {c}'.format(gamma = b, c = i))
	# 		score2 = cross_validation.cross_val_score(clf2, unit_var_0_feature0_without, Array[1], cv = 5)
	# 		print(score2)
	# 		print(score2.mean())
	# 		print('This is unit variance on noe ratio gamma {gamma} and C {c}'.format(gamma = b, c = i))

	# for i in range(100, 500, 50):
	# 	clf = RandomForestClassifier(n_estimators = i, min_samples_split = 1)
	# 	clf2 = RandomForestClassifier(n_estimators = i, min_samples_split = 1)
	# 	score = cross_validation.cross_val_score(clf, unit_var_0_feature, Array[1], cv = 5)
	# 	score2 = cross_validation.cross_val_score(clf2, Array[0], Array[1], cv = 5)
	# 	print(score)
	# 	print(score.mean())
	# 	print('Random Forest of Trees n_estimator {n_estimate} and scaled data'.format(n_estimate = i))
	# 	print(score2)
	# 	print(score2.mean())
	# 	print('Random Forest of Trees n_estimator {n_estimate} and non scaled data'.format(n_estimate = i))
	# clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
	# clf2 = RandomForestClassifier(n_estimators = 10000, min_samples_split = 1)
	# clf3 = RandomForestClassifier(n_estimators = 75, min_samples_split = 1)
	# clf4 = RandomForestClassifier(n_estimators = 75, min_samples_split = 2)
	# score = cross_validation.cross_val_score(clf, Array[0], Array[1], cv = 5)
	# score2 = cross_validation.cross_val_score(clf2, Array[0], Array[1], cv = 5)
	# score3 = cross_validation.cross_val_score(clf3, Array[0], Array[1], cv = 5)
	# score4 = cross_validation.cross_val_score(clf4, Array[0], Array[1], cv = 5)
	# print(score)
	# print(score.mean())
	# print(score2)
	# print(score2.mean())
	# print(score3)
	# print(score3.mean())
	# print(score4)
	# print(score4.mean())
	for i in range(100):
		print(Array[0][i])
		print(Array[1][i])


def CompareTest(databaseFun, databaseTest, total_Array):
	print(len(total_Array[0]))
	data_Array = compile_feature_list_sb(databaseTest, databaseFun)
	total_Array2 = [data_Array[0], data_Array[1]]
	print(len(total_Array[0]))
	# total_Array[0] += data_Array[0]
	# total_Array[1] += data_Array[1]
	training_vector = []
	target_vector = []
	length = len(total_Array2[0])
	print(length)
	count = 0
	for i in range(length):
		if total_Array2[0][i][0] > 800  and total_Array2[1][i] == 0:
			count += 1
			pass
		else:
			training_vector.append(total_Array2[0][i])
			target_vector.append(total_Array2[1][i])
	clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
	clf.fit(total_Array[0], total_Array[1])
	correct = 0
	for i in range(len(total_Array2[0])):
		prediction = clf.predict([total_Array2[0][i]])
		if prediction[0] == total_Array2[1][i]:
			correct += 1
	print((float(correct)/len(data_Arrays[1])) * 100)
	clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
	score = cross_validation.cross_val_score(clf, total_Array[0] + total_Array2[0], total_Array[1] + total_Array2[1], cv = 5)
	# unit_var_0_feature = total_Array[0]
	# unit_var_0_feature = preprocessing.scale(unit_var_0_feature)
	# clf = svm.SVC()
	# score = cross_validation.cross_val_score(clf, unit_var_0_feature, total_Array[1], cv = 5)

	print(score.mean())
	print(score.std())
def specific():
	
	file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = 'Pilcr1'), 'rb')
	data_Arrays = pickle.load(file)
	# data_Arrays = compile_feature_list_sb('Anasp1', 'Pirfi3')
	min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	training_vector = []
	target_vector = []
	length = len(data_Arrays[0])
	count = 0
	for i in range(length):
		if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
			count += 1
			pass
		elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
			pass
		else:
			training_vector.append(data_Arrays[0][i])
			target_vector.append(data_Arrays[1][i])
	print(count)
	# total_Array[0] += data_Arrays[0]
	# total_Array[1] += data_Arrays[1]
	non_scaled = list(training_vector)
	training_vector = list(min_max_scale.fit_transform(training_vector))
	print(training_vector[0])
	total_Array = [training_vector, target_vector]
	file.close()
	file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = 'Fibsp1'), 'rb')
	min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	data_Arrays = pickle.load(file)
	# data_Arrays = compile_feature_list_sb('Neosp1', 'Pirfi3')
	training_vector = []
	target_vector = []
	length = len(data_Arrays[0])
	count = 0
	for i in range(length):
		if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
			count += 1
			pass
		elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
			pass
		else:
			training_vector.append(data_Arrays[0][i])
			target_vector.append(data_Arrays[1][i])
	print(count)
	non_scaled += list(training_vector)
	training_vector = list(min_max_scale.fit_transform(training_vector))
	total_Array[0] += training_vector
	total_Array[1] += target_vector
	file.close()
	# file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = 'Dekbr1'), 'rb')
	# data_Arrays = pickle.load(file)
	# min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	# training_vector = []
	# target_vector = []
	# length = len(data_Arrays[0])
	# count = 0
	# for i in range(length):
	# 	if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
	# 		count += 1
	# 		pass
	# 	elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
	# 		pass
	# 	else:
	# 		training_vector.append(data_Arrays[0][i])
	# 		target_vector.append(data_Arrays[1][i])
	# print(count)
	# non_scaled += list(training_vector)
	# total_Array[0] += list(min_max_scale.fit_transform(training_vector))
	# total_Array[1] += target_vector
	# file.close()
	# file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = 'Hanpo2'), 'rb')
	# data_Arrays = pickle.load(file)
	# # data_Arrays = compile_feature_list_sb('Hanva1_1', 'Pirfi3')
	# min_max_scale = preprocessing.MinMaxScaler((-1, 1))
 # 	training_vector = []
	# target_vector = []
	# length = len(data_Arrays[0])
	# count = 0
	# for i in range(length):
	# 	if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
	# 		count += 1
	# 		pass
	# 	elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
	# 		pass
	# 	else:
	# 		training_vector.append(data_Arrays[0][i])
	# 		target_vector.append(data_Arrays[1][i])
	# print(count)
	# non_scaled += list(training_vector)
	# total_Array[0] += list(min_max_scale.fit_transform(training_vector))
	# total_Array[1] += target_vector
	# file.close()
	# file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = 'Hydru2'), 'rb')
	# data_Arrays = pickle.load(file)
	# # data_Arrays = compile_feature_list_sb('Conth1', 'Pirfi3')
	# min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	# training_vector = []
	# target_vector = []
	# length = len(data_Arrays[0])
	# count = 0
	# for i in range(length):
	# 	if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
	# 		count += 1
	# 		pass
	# 	elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
	# 		pass
	# 	else:
	# 		training_vector.append(data_Arrays[0][i])
	# 		target_vector.append(data_Arrays[1][i])
	# print(count)
	# non_scaled += list(training_vector)
	# total_Array[0] += list(min_max_scale.fit_transform(training_vector))
	# total_Array[1] += target_vector
	# file.close()
	# file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = 'Tulca1'), 'rb')
	# data_Arrays = pickle.load(file)
	# # data_Arrays = compile_feature_list_sb('PirE2_1', 'Pirfi3')
	# min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	# training_vector = []
	# target_vector = []
	# length = len(data_Arrays[0])
	# count = 0
	# for i in range(length):
	# 	if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
	# 		count += 1
	# 		pass
	# 	elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
	# 		pass
	# 	else:
	# 		training_vector.append(data_Arrays[0][i])
	# 		target_vector.append(data_Arrays[1][i])
	# print(count)
	# non_scaled += list(training_vector)
	# total_Array[0] += list(min_max_scale.fit_transform(training_vector))
	# total_Array[1] += target_vector
	# file.close()
	# print(len(total_Array[0]))
	# file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = 'Helsul1'), 'rb')
	# data_Arrays = pickle.load(file)
	# # data_Arrays = compile_feature_list_sb('PirE2_1', 'Pirfi3')
	# min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	# training_vector = []
	# target_vector = []
	# length = len(data_Arrays[0])
	# count = 0
	# for i in range(length):
	# 	if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
	# 		count += 1
	# 		pass
	# 	elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
	# 		pass
	# 	else:
	# 		training_vector.append(data_Arrays[0][i])
	# 		target_vector.append(data_Arrays[1][i])
	# print(count)
	# non_scaled += list(training_vector)
	# total_Array[0] += list(min_max_scale.fit_transform(training_vector))
	# total_Array[1] += target_vector
	# file.close()
	# print(len(total_Array[0]))
	# file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = 'Pirfi3'), 'rb')
	# data_Arrays = pickle.load(file)
	# # data_Arrays = compile_feature_list_sb('Conth1', 'Pirfi3')
	# min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	# training_vector = []
	# target_vector = []
	# length = len(data_Arrays[0])
	# count = 0
	# for i in range(length):
	# 	if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
	# 		count += 1
	# 		pass
	# 	elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
	# 		pass
	# 	else:
	# 		training_vector.append(data_Arrays[0][i])
	# 		target_vector.append(data_Arrays[1][i])
	# print(count)
	# non_scaled += list(training_vector)
	# total_Array[0] += list(min_max_scale.fit_transform(training_vector))
	# total_Array[1] += target_vector
	# file.close()
	# file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = 'Spoth2'), 'rb')
	# data_Arrays = pickle.load(file)
	# # data_Arrays = compile_feature_list_sb('PirE2_1', 'Pirfi3')
	# min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	# training_vector = []
	# target_vector = []
	# length = len(data_Arrays[0])
	# count = 0
	# for i in range(length):
	# 	if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
	# 		count += 1
	# 		pass
	# 	elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
	# 		pass
	# 	else:
	# 		training_vector.append(data_Arrays[0][i])
	# 		target_vector.append(data_Arrays[1][i])
	# print(count)
	# non_scaled += list(training_vector)
	# total_Array[0] += list(min_max_scale.fit_transform(training_vector))
	# total_Array[1] += target_vector
	# file.close()
	# print(len(total_Array[0]))
	# file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = 'Neosp1'), 'rb')
	# data_Arrays = pickle.load(file)
	# # data_Arrays = compile_feature_list_sb('PirE2_1', 'Pirfi3')
	# min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	# training_vector = []
	# target_vector = []
	# length = len(data_Arrays[0])
	# count = 0
	# for i in range(length):
	# 	if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
	# 		count += 1
	# 		pass
	# 	elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
	# 		pass
	# 	else:
	# 		training_vector.append(data_Arrays[0][i])
	# 		target_vector.append(data_Arrays[1][i])
	# print(count)
	# non_scaled += list(training_vector)
	# total_Array[0] += list(min_max_scale.fit_transform(training_vector))
	# total_Array[1] += target_vector
	# file.close()
	# file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = 'Thihy1'), 'rb')
	# data_Arrays = pickle.load(file)
	# # data_Arrays = compile_feature_list_sb('PirE2_1', 'Pirfi3')
	# min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	# training_vector = []
	# target_vector = []
	# length = len(data_Arrays[0])
	# count = 0
	# for i in range(length):
	# 	if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
	# 		count += 1
	# 		pass
	# 	elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
	# 		pass
	# 	else:
	# 		training_vector.append(data_Arrays[0][i])
	# 		target_vector.append(data_Arrays[1][i])
	# print(count)
	# non_scaled += list(training_vector)
	# total_Array[0] += list(min_max_scale.fit_transform(training_vector))
	# total_Array[1] += target_vector
	# file.close()
	# print(len(total_Array[0]))
	# file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = 'Myche1'), 'rb')
	# data_Arrays = pickle.load(file)
	# # data_Arrays = compile_feature_list_sb('PirE2_1', 'Pirfi3')
	# min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	# training_vector = []
	# target_vector = []
	# length = len(data_Arrays[0])
	# count = 0
	# for i in range(length):
	# 	if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
	# 		count += 1
	# 		pass
	# 	elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
	# 		pass
	# 	else:
	# 		training_vector.append(data_Arrays[0][i])
	# 		target_vector.append(data_Arrays[1][i])
	# print(count)
	# non_scaled += list(training_vector)
	# total_Array[0] += list(min_max_scale.fit_transform(training_vector))
	# total_Array[1] += target_vector
	# file.close()
	# print(len(total_Array[0]))
	
	# print(len(total_Array[0]))
	# print(len(total_Array[0]))
	# clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
	# clf.fit(total_Array[0], total_Array[1])
	# clf2 = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
	# clf2.fit(non_scaled, total_Array[1])
	# data_Arrays = compile_feature_list_sb('Mutel1', 'Rhihy1')
	# min_max_scale = preprocessing.MinMaxScaler((-1, 1))
	# target_vector = []
	# training_vector = []
	# for i in range(len(data_Arrays[0])):
	# 	if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
	# 		pass
	# 	elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
	# 		pass
	# 	else:
	# 		training_vector.append(data_Arrays[0][i])
	# 		target_vector.append(data_Arrays[1][i])
	# non_scaled_test = list(training_vector)
	# data_Arrays = (min_max_scale.fit_transform(list(training_vector)), target_vector)
	# correct = 0
	# for i in range(len(data_Arrays[0])):
	# 	prediction = clf.predict([data_Arrays[0][i]])
	# 	if prediction[0] == data_Arrays[1][i]:
	# 		correct += 1
	# print((float(correct)/len(data_Arrays[1])) * 100)
	# correct = 0
	# for i in range(len(data_Arrays[0])):
	# 	prediction = clf2.predict([non_scaled_test[i]])
	# 	if prediction[0] == data_Arrays[1][i]:
	# 		correct += 1
	# print((float(correct)/len(data_Arrays[1])) * 100)
    
	clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
	clf2 = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
	score = cross_validation.cross_val_score(clf, total_Array[0], total_Array[1], cv = 10)
	score2 = cross_validation.cross_val_score(clf2, non_scaled, total_Array[1], cv = 10)

	print(score)
	print(score.mean())
	print(score2)
	print(score2.mean())
	clf3 = svm.SVC()
	unit_var_0_feature = preprocessing.scale(non_scaled)
	score3 = cross_validation.cross_val_score(clf3, unit_var_0_feature, total_Array[1], cv = 10)
	print(score3)
	print(score3.mean())
	clf4 = svm.SVC()
	unit_var_0_feature1 = preprocessing.scale(total_Array[0])
	score4 = cross_validation.cross_val_score(clf4, unit_var_0_feature1, total_Array[1], cv = 10)
	print(score4)
	print(score4.mean())

database = sys.argv[2]
file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = database), 'rb')
data_Arrays = pickle.load(file)
file.close()
# split = len(data_Arrays[0]) - 300 
# model = [data_Arrays[0][i] for i in range(split)]
# target = [data_Arrays[1][i] for i in range(split)]
# training_Arrays = (model, target)
# model = [data_Arrays[0][i] for i in range(split, len(data_Arrays[0]))]
# target = [data_Arrays[1][i] for i in range(split, len(data_Arrays[0]))]
# testing_Arrays = (model, target)
command = sys.argv[1]
if command == "cross_val":
	Cross_Validation_Test(data_Arrays)
elif command == "specific":
	specific()
elif command == "outlier":
	count = 0
	for i in range(len(data_Arrays[0])):
		if data_Arrays[0][i][0] > 850 and data_Arrays[1][i] == 0:
			count += 1
	print(count)
elif command == "gold":
	target_vector = []
	training_vector = []
	print(len(data_Arrays[0]))
	for i in range(len(data_Arrays[0])):
		if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
			pass
		elif data_Arrays[0][i][0] < 100 and data_Arrays[1][i] == 1:
			pass
		else:
			training_vector.append(data_Arrays[0][i])
			target_vector.append(data_Arrays[1][i])
	correct = 0
	for i in range(len(target_vector)):
		if training_vector[i][0] > 450 and target_vector[i] == 1:
			correct += 1
		elif training_vector[i][0] <= 450 and target_vector[i] == 0:
			correct += 1
		else:
			pass
	print((float(correct)/len(training_vector)) * 100)
else:
	databaseTest = sys.argv[3]
	CompareTest(database, databaseTest, data_Arrays)
