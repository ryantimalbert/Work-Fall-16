import sys
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm, cross_validation, preprocessing
p_fam_table = sys.argv[1]
table = open(p_fam_table, 'r')
lines = table.readlines()
table.close()
PFAM_Parse = []
for line in lines:
	line = line.split()
	PFAM_Parse.append([line[0], line[2 ::]])
### 98 different features for selection
index = PFAM_Parse[0][1]
features = PFAM_Parse[1 ::]
Genomes = {}
for count in range(len(index)):
	genome = index[count]
	Genomes[genome] = [[]]
	for line in features:
		Genomes[genome][0].append(line[1][count])
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
		Genomes[genome].append(0)
		checked_genomes.append(genome)
	elif 'pathogen' in line or 'Pathogen' in line:
		Genomes[genome].append(1)
		checked_genomes.append(genome)

cluster_table = sys.argv[3]
table = open(cluster_table, 'r')
lines = table.readlines()
table.close()
Cluster_Parse = []
for line in lines[1::]:
	line = line.split()
	Cluster_Parse.append([line[0], line[1 ::]])

index = lines[0].split()
features = Cluster_Parse
Cluster_Genome = {}
for count in range(len(index)):
	genome = index[count]
	Cluster_Genome[genome] = [[]]
	for line in features:
		Cluster_Genome[genome][0].append(line[1][count])

target = []
features = []
for genome in Genomes:
	if genome in checked_genomes:
		target.append(Genomes[genome][1])
		features.append(Genomes[genome][0])

target2 = []
features2 = []
for genome in Cluster_Genome:
	if genome in checked_genomes:
		target2.append(Genomes[genome][1])
		features2.append(Cluster_Genome[genome][0])

#### Print used pfamId's
clf = ExtraTreesClassifier()
clf = clf.fit(features, target)
weight_array = clf.feature_importances_
valued_p_fam = []
count = 0
PFAM = PFAM_Parse[1 ::]
for num in weight_array:
	if num != 0:
	    valued_p_fam.append(PFAM[count][0])	
	count += 1	
# print(valued_p_fam)
print(len(valued_p_fam))
print(len(weight_array))

### Print used ClusterId's
clf2 = ExtraTreesClassifier()
clf2 = clf.fit(features2, target2)
weight_array2 = clf2.feature_importances_
valued_cluster = []
count = 0
for num in weight_array2:
	if num != 0:
	    valued_cluster.append(Cluster_Parse[count][0])
	count += 1	
# print(valued_cluster)
print(len(valued_cluster))
print(len(weight_array2))


new_features = []
for i in features:
	new_features.append([])
new_features2 = []
for i in features2:
	new_features2.append([])
count = 0
for num in weight_array:
	if num != 0:
		count2 = 0
		for i in features:
			new_features[count2].append(features[count2][count])
			count2 += 1
	count += 1
count = 0
for num in weight_array2:
	if num != 0:
		count2 = 0
		for i in features:
			new_features2[count2].append(features2[count2][count])
			count2 += 1
	count += 1
print(len(new_features[0]))
print(len(new_features2[0]))
print(len(target))

clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
score = cross_validation.cross_val_score(clf, features, target, cv = 15)
print(score.mean())
print(score.std())

clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
score = cross_validation.cross_val_score(clf, features2, target2, cv = 15)
print(score.mean())
print(score.std())

clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
score = cross_validation.cross_val_score(clf, new_features, target, cv = 15)
print(score.mean())
print(score.std())

clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
score = cross_validation.cross_val_score(clf, new_features2, target2, cv = 15)
print(score.mean())
print(score.std())

combined = []
for count in range(len(new_features)):
	lis = new_features[count] + new_features2[count]
	combined.append(lis)

clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
score = cross_validation.cross_val_score(clf, combined, target2, cv = 15)
print(score.mean())
print(score.std())

