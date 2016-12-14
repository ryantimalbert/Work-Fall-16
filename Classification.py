import os
from sklearn import svm, cross_validation, preprocessing
from sklearn.feature_selection import SelectKBest
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

X_new = SelectKBest(k=9)
X_new = X_new.fit(new_features, target)
correct = X_new.get_support()
scores = X_new.scores_
count = 0
best_features = []
feature_index = []
best_scores = []
for i in features:
	best_features.append([])
for bol in correct:
	if bol:
		feature_index.append(count)
		best_scores.append(scores[count])
		for count2 in range(len(new_features)):
			best_features[count2].append(new_features[count2][count])
	count += 1
top_9 = []
for count in range(len(best_scores)):
	top_9.append((feature_index[count], best_scores[count]))
top_9 = sorted(top_9, key = lambda k : k[1])
top_9.reverse()
for i in top_9:
	print(i)
clf = svm.SVC()
score = cross_validation.cross_val_score(clf, best_features, target, cv = 5)
print(score.mean())
print(score.std())

file1 = open('strain.txt', 'r')
lines = file1.readlines()
feature = []
count = 0
for line in lines:
	line = line.split()
	for l in line:
		if '(' in l:
			l = l.replace('(', '')
			l = l.replace(')', '')
			if count in feature_index:
				feature.append(l)
	count += 1
clf = svm.SVC()
clf.fit(best_features, target)
print(clf.predict([feature]))
print(len(best_features))
for b in best_features:
	b[6] = b[6] * 10
	b[7] = b[7] * 3
clf = svm.SVC()
score = cross_validation.cross_val_score(clf, best_features, target, cv = 5)
print(score.mean())
print(score.std())

clf = svm.SVC()
clf.fit(best_features, target)
print(clf.predict([feature]))

