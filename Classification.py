import os
from sklearn.svm import SVC
from sklearn import preprocessing
features = []
target = []
bio_remidiate = os.listdir('Bio_Remediated:Taylor')
for f in bio_remidiate:
	if f == '.DS_Store':
		continue;
	fil = open('Bio_Remediated:Taylor/' + f, 'r')
	lines = fil.readlines()
	target.append(1)
	feature = []
	for line in lines:
		line = line.split()
		for l in line:
			if '(' in l:
				l = l.replace('(', '')
				l = l.replace(')', '')
				feature.append(l)
	features.append(feature)

plant = os.listdir('Plant_Based:Diego')
for f in plant:
	if f == '.DS_Store':
		continue;
	fil = open('Plant_Based:Diego/' + f, 'r')
	lines = fil.readlines()
	target.append(0)
	feature = []
	for line in lines:
		line = line.split()
		for l in line:
			if '(' in l:
				l = l.replace('(', '')
				l = l.replace(')', '')
				feature.append(l)
	features.append(feature)


clf = svm.SVC()
score = cross_validation.cross_val_score(clf, features, target, cv = 5)
print(score.mean())
print(score.std())

new_features = preprocessing.scale(features)
clf = svm.SVC()
score = cross_validation.cross_val_score(clf, new_features, target, cv = 5)
print(score.mean())
print(score.std())

