import cPickle as pickle
from sklearn import svm, cross_validation, preprocessing
import sys
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.lda import LDA
from sklearn.metrics import roc_curve, auc
import csv
import numpy
def train_LDA(Array):
	clf = LDA()
	unit_var_0_feature = Array[0]
	unit_var_0_feature = preprocessing.scale(unit_var_0_feature)
	score = cross_validation.cross_val_score(clf, unit_var_0_feature, Array[1], cv = 5)
	print(score.mean())
	print(score.std())
def train_SVM(Array):
	unit_var_0_feature = Array[0]
	unit_var_0_feature = preprocessing.scale(unit_var_0_feature)
	clf = svm.SVC()
	score = cross_validation.cross_val_score(clf, unit_var_0_feature, Array[1], cv = 5)
	print(score.mean())
	print(score.std())

def train_RFT(Array):
	clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
	score = cross_validation.cross_val_score(clf, Array[0], Array[1], cv = 5)
	print(score.mean())
	print(score.std())

def Test_Reload(Array, database):
	file = open('02f02485ab679a9031f461bdbd3edab48ea42a79/{database}.txt'.format(database = database), 'rb')
	clf = pickle.load(file)
	file.close()
	test_total_set(Array, clf)

def Save_ML(Array, database):
	clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
	clf.fit(Array[0], Array[1])
	test_total_set(Array, clf)
	file = open('/{database}.txt'.format(database = database), 'wb')
	serialized = pickle.dumps(clf)
	file.write(serialized)
	file.close()

def test_total_set(Array, clf):
	correct = 0
	count = 0
	for i in range(len(Array[0])):
		prediction = clf.predict([Array[0][i]])
		if prediction[0] == Array[1][i]:
			correct += 1
		count += 1
		print(count)
	print((float(correct)/len(Array[0])) * 100)
def roc_curve_calc(Array):
	# unit_var_0_feature = Array[0]
	# unit_var_0_feature = preprocessing.scale(unit_var_0_feature)
	training = []
	target = []
	split= int(len(data_Arrays[0]) * .8)
	clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
	for i in range(split):
		training.append(data_Arrays[0][i])
		target.append(data_Arrays[1][i])
	clf.fit(training, target)
	training_test = []
	target_test = []
	for i in range(split, len(data_Arrays[0])):
		training_test.append(data_Arrays[0][i])
		target_test.append(data_Arrays[1][i])
	probabilities = clf.predict_proba(training_test)
	pos_prob = []
	for i in range(len(probabilities)):
		pos_prob.append(probabilities[i][1])	
	fpr, tpr, thresholds = roc_curve(target_test, pos_prob, pos_label = 1)
	print(len(fpr))
	print(len(tpr))
	mean_fpr = 0
	for i in fpr:
		mean_fpr += i
	mean_fpr = mean_fpr / float(len(fpr))
	print(mean_fpr)
	mean_tpr = 0
	for j in tpr:
		mean_tpr += j
	mean_tpr = mean_tpr / float(len(tpr))
	print(mean_tpr)
	print(auc(fpr, tpr))
	return (fpr, tpr)
def outlier_reduction(data_Arrays):
	training_vector = []
	target_vector = []
	length = len(data_Arrays[0])
	for i in range(length):
		if data_Arrays[0][i][0] > 800  and data_Arrays[1][i] == 0:
			pass
		elif data_Arrays[0][i][0] < 100  and data_Arrays[1][i] == 1:
			pass
		else:
			training_vector.append(data_Arrays[0][i])
			target_vector.append(data_Arrays[1][i])
	return (training_vector, target_vector)

def build():
	built_data = {}
	file = open('TestingDBs.txt', 'r')
	file_read = file.readlines()
	count = 0
	for line in file_read:
		line = line.strip()
		built_data[line] =  []
		file2 = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = line), 'rb')
		data_Arrays = pickle.load(file2)
		file2.close()
		Array = outlier_reduction(data_Arrays)
		clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
		score = cross_validation.cross_val_score(clf, Array[0], Array[1], cv = 5)
		RTF_score = score.mean()
		unit_var_0_feature = list(Array[0])
		unit_var_0_feature = preprocessing.scale(unit_var_0_feature)
		clf = svm.SVC()
		score2 = cross_validation.cross_val_score(clf, unit_var_0_feature, Array[1], cv = 5)
		SVM_score = score2.mean()
		built_data[line].append(RTF_score)
		built_data[line].append(SVM_score)
		if RTF_score > SVM_score:
			built_data[line].append("RTF")
		else:
			built_data[line].append("SVM")
		correct = 0
		for i in range(len(Array[0])):
			if Array[0][i][0] > 450 and Array[1][i] == 1:
				correct += 1
			elif Array[0][i][0] <= 450 and Array[1][i] == 0:
				correct += 1
			else:
				pass
		built_data[line].append(float(correct)/len(Array[0]))
		count += 1
		print(count)
	save_file = open('built_data.txt', 'wb')
	serialized = pickle.dumps(built_data)
	save_file.write(serialized)
	file.close()
	save_file.close()

def read():
	file = open('built_data.txt', 'rb')
	data_readable = pickle.load(file)
	file.close()
	file2 = open('original_score.txt', 'w+')
	for genome in data_readable:
		file2.write(genome)
		file2.write(str(data_readable[genome]) + '\n')
	file2.close()
	# best = []
	# gold_standard = []
	# SVM = 0
	# RTF = 0
	# for name in data_readable:
	# 	if data_readable[name][2] == "SVM":
	# 		point = data_readable[name][1]
	# 		best.append(point * 100)
	# 		SVM += 1
	# 	else:
	# 		point = data_readable[name][0]
	# 		best.append(point * 100)
	# 		RTF += 1
	# 	point = data_readable[name][3]
	# 	gold_standard.append(point * 100)
	# best = numpy.array(best)
	# gold_standard = numpy.array(gold_standard)
	# print(numpy.mean(best))
	# print(numpy.std(best))
	# print(numpy.mean(gold_standard))
	# print(numpy.std(gold_standard))
	# print(SVM)
	# print(RTF)

def add():
	file = open('built_data.txt', 'rb')
	built_data = pickle.load(file)
	file_read = ['Anasp1'] ## what data points should be added or changed
	for line in file_read:
		built_data[line] =  []
		file2 = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = line), 'rb')
		data_Arrays = pickle.load(file2)
		file2.close()
		Array = outlier_reduction(data_Arrays)
		clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
		score = cross_validation.cross_val_score(clf, Array[0], Array[1], cv = 5)
		RTF_score = score.mean()
		unit_var_0_feature = list(Array[0])
		unit_var_0_feature = preprocessing.scale(unit_var_0_feature)
		clf = svm.SVC()
		score2 = cross_validation.cross_val_score(clf, unit_var_0_feature, Array[1], cv = 5)
		SVM_score = score2.mean()
		built_data[line].append(SVM_score)
		built_data[line].append(RTF_score)
		if RTF_score > SVM_score:
			built_data[line].append("RTF")
		else:
			built_data[line].append("SVM")
		correct = 0
		for i in range(len(Array[0])):
			if Array[0][i][0] > 450 and Array[1][i] == 1:
				correct += 1
			elif Array[0][i][0] <= 450 and Array[1][i] == 0:
				correct += 1
			else:
				pass
		built_data[line].append(float(correct)/len(Array[0]))
	save_file = open('built_data.txt', 'wb')
	serialized = pickle.dumps(built_data)
	save_file.write(serialized)
	save_file.close()

def CSV():
	read_file = open('built_data.txt', 'rb')
	data_readable = pickle.load(read_file)
	read_file.close()
	file = open('Scatter.csv', 'wb')
	writer = csv.writer(file, quoting=csv.QUOTE_ALL)
	array = []
	for name in data_readable:
		internal_array = []
		internal_array.append(name)
		point = data_readable[name][0]
		internal_array.append(point * 100)
		point = data_readable[name][1]
		internal_array.append(point * 100)
		point = data_readable[name][3]
		internal_array.append(point * 100)
		writer.writerow(internal_array)
	# fpr_tpr = roc_curve_calc(data_Arrays)
	# file = open('roc_Anasp.csv', 'wb')
	# writer = csv.writer(file, quoting=csv.QUOTE_ALL)
	# for num in range(len(fpr_tpr[0])):
	# 	internal_array = []
	# 	internal_array.append(fpr_tpr[0][num])
	# 	internal_array.append(fpr_tpr[1][num])
	# 	writer.writerow(internal_array)
	# file.close()



database = sys.argv[2]
file = open('features/2ca94f869f91c32d28c5a7074b718204e67f2034/{database}.txt'.format(database = database), 'rb')
data_Arrays = pickle.load(file)
file.close()
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
data_Arrays = (training_vector, target_vector)
command = sys.argv[1]
if command == "SVM":
	train_SVM(data_Arrays)
elif command == "RTF":
	train_RFT(data_Arrays)
elif command == "save":
	Save_ML(data_Arrays, database)
elif command == "LDA":
	train_LDA(data_Arrays)
elif command == "roc_curve":
	roc_curve_calc(data_Arrays)
elif command == "build":
	build()
elif command == 'read':
	read()
elif command == 'add':
	add()
elif command == 'csv':
	CSV()
else:
	Test_Reload(data_Arrays, database)