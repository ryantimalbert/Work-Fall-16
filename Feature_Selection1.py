import sys
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm, cross_validation, preprocessing
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import SVC
from sklearn.feature_selection import RFECV
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from sklearn.svm import SVC
import numpy
p_fam_table = sys.argv[1]
table = open(p_fam_table, 'r')
lines = table.readlines()
table.close()
PFAM_Parse = []

####### FOR PFAM
for line in lines:
	line = line.split()
	PFAM_Parse.append([line[0], line[2 ::]])
### 98 different features for selection
index = PFAM_Parse[0][1]
features = PFAM_Parse[1 ::]


# ####### FOR CLUSTER
# index = lines[0].split()
# for line in lines[1 ::]:
# 	line = line.split()
# 	PFAM_Parse.append([line[0], line[1 ::]])
# features = PFAM_Parse


Genomes = []
print(len(PFAM_Parse[0][1]))
for count in range(len(index)):
	genome = index[count]
	fet = []
	for line in features:
		fet.append(line[1][count])
	Genomes.append([genome, fet])
life_style = sys.argv[2]
style = open(life_style, 'r')
lines = style.readlines()
style.close()
count = 0
checked_genomes = []
for line in lines:
	line = line.split()
	genome = line[0]
	if 'Saprobe' in line:
		for i in Genomes:
			if i[0] == genome:
				i.append(0)
		checked_genomes.append(genome)
	elif 'pathogen' in line or 'Pathogen' in line:
		for i in Genomes:
			if i[0] == genome:
				i.append(1)
		checked_genomes.append(genome)
	else:
		pass



target = []
features = []
count1 = 0
for genome in Genomes:
	if genome[0] in checked_genomes:
		target.append(genome[2])
		features.append(genome[1])
	else:
		count1 += 1
print(count1)
print(len(features))





X_new = SelectKBest(k=100)
X_new = X_new.fit(features, target)
correct = X_new.get_support()
count = 0

## for PFAM
PFAM = PFAM_Parse[1 ::]

# ### for Cluster
# PFAM = PFAM_Parse

out_file = open('result_PFAM.txt', 'wb')
best_scores = []
best_features = []
new_features = []
for i in features:
	new_features.append([])
for bol in correct:
	if bol:
		best_features.append(PFAM[count])
		best_scores.append(X_new.scores_[count])
		for count2 in range(len(new_features)):
			new_features[count2].append(features[count2][count])
	count += 1
count = 0
out_file.write('Top 100 features ranked \n')
top_100 = []
for count in range(len(best_scores)):
	top_100.append((best_features[count][0], best_scores[count]))
	# elif best_features[count][0] == '7663':
	# 	print(best_features[count])
	# 	print(best_scores[count])
top_100 = sorted(top_100, key = lambda k : k[1])
top_100.reverse()
for i in range(len(top_100)):
	out_file.write(str(i + 1) + ' ' + top_100[i][0] + '\n')
out_file.close()


####### Test
# print(best_features[0][0])
# for i in new_features:
# 	print(i[0])


clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
score = cross_validation.cross_val_score(clf, new_features, target, cv = 15)
print(score.mean())
print(score.std())



















# for val in valued_p_fam:
# 	print(val)
# print(PFAM[4556][0])
# for i in range(len(features)):
# 	print(features[i][4556])
# 	print(target[i])
# for num in weight_array:
# 	if num != 0:
# 		count2 = 0
# 		for i in features:
# 			new_features[count2].append(features[count2][count])
# 			count2 += 1

# target2 = []
# features2 = []
# for genome in Cluster_Genome:
# 	if genome in checked_genomes:
# 		target2.append(Genomes[genome][1])
# 		features2.append(Cluster_Genome[genome][0])

#### Print used pfamId's
# clf = ExtraTreesClassifier()
# clf = clf.fit(features, target)

# weight_array = clf.feature_importances_
# valued_p_fam = []
# new_weights = []
# count = 0
# PFAM = PFAM_Parse[1 ::]
# for num in weight_array:
# 	if num != 0:
# 	    valued_p_fam.append(PFAM[count][0])
# 	    new_weights.append(num)
# 	count += 1

# for p_fam in valued_p_fam:
# 	print(p_fam)
# print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
## Print used ClusterId's
# clf2 = ExtraTreesClassifier()
# clf2 = clf.fit(features2, target2)
# weight_array2 = clf2.feature_importances_
# valued_cluster = []
# new_weights2 = []
# count = 0
# for num in weight_array2:
# 	if Cluster_Parse[count][0] == '7663':
# 		print(Cluster_Genome['Settu1'][0][count])
# 		print(Genomes['Settu1'][1])
# 		print(Genomes['Settu1'][0][count])
# 		print(Cluster_Genome['Zymps1'][0][count])
# 		print(Genomes['Zymps1'][1])
# 		print(Genomes['Zymps1'][0][count])
# 		print(num)
# 	if num != 0:
# 	    valued_cluster.append(Cluster_Parse[count][0])
# 	    new_weights2.append(num)
# 	count += 1

# for cluster in valued_cluster:
# 	print(cluster)
# print('===================================================================')

# mean1 = numpy.mean(new_weights)
# std1 = numpy.std(new_weights)
# for count in range(len(new_weights)):
# 	if new_weights[count] >= mean1 + (2 * std1):
# 		print(valued_p_fam[count])

# mean1 = numpy.mean(new_weights2)
# std1 = numpy.std(new_weights2)
# for count in range(len(new_weights2)):
# 	if new_weights2[count] >= mean1 + (2 * std1):
# 		print(valued_cluster[count])

# for value in valued_cluster:
# 	if value == '7663':
# 		print("HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

# new_features = []
# bad_features = []
# for i in features:
# 	new_features.append([])
# 	bad_features.append([])
# new_features2 = []
# bad_features2 = []
# for i in features2:
# 	new_features2.append([])
# 	bad_features2.append([])
# count = 0
# for num in weight_array:
# 	if num != 0:
# 		count2 = 0
# 		for i in features:
# 			new_features[count2].append(features[count2][count])
# 			count2 += 1
# 	else :
# 		count2 = 0
# 		for i in features:
# 			bad_features[count2].append(features[count2][count])
# 			count2 += 1
# 	count += 1
# count = 0
# print(len(weight_array2))
# for num in weight_array2:
# 	if num != 0:
# 		count2 = 0
# 		for i in features:
# 			new_features2[count2].append(features2[count2][count])
# 			count2 += 1
# 	else:
# 		count2 = 0
# 		for i in features:
# 			bad_features2[count2].append(features2[count2][count])
# 			count2 += 1
# 	count += 1
# print(len(new_features[0]))
# print(len(new_features2[0]))
# print(len(bad_features[0]))
# print(len(bad_features2[0]))
# print(len(target))


# clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
# score = cross_validation.cross_val_score(clf, bad_features, target, cv = 15)
# print(score.mean())
# print(score.std())

# clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
# score = cross_validation.cross_val_score(clf, bad_features2, target2, cv = 15)
# print(score.mean())
# print(score.std())

# clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
# score = cross_validation.cross_val_score(clf, new_features, target, cv = 15)
# print(score.mean())
# print(score.std())

# clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
# score = cross_validation.cross_val_score(clf, new_features2, target2, cv = 15)
# print(score.mean())
# print(score.std())

# clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
# score = cross_validation.cross_val_score(clf, new_features2, target2, cv = 15)
# print(score.mean())
# print(score.std())

# combined = []
# for count in range(len(new_features)):
# 	lis = new_features[count] + new_features2[count]
# 	combined.append(lis)

# clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
# score = cross_validation.cross_val_score(clf, combined, target2, cv = 15)
# print(score.mean())
# print(score.std())

# X_new = SelectKBest(chi2, k= 100).fit_transform(features, target)
# clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
# score = cross_validation.cross_val_score(clf, X_new, target, cv = 15)
# print(score.mean())
# print(score.std())