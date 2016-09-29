from sklearn.ensemble import RandomForestClassifier
from sklearn import svm, cross_validation, preprocessing
import numpy
ATG_Conservation = open('ATG_Con_Out_Neucr2', 'r')
Secondary_Structure = open('secondary_out.txt', 'r')
ATG_lines = ATG_Conservation.readlines()
Secondary_lines = Secondary_Structure.readlines()
secondary_training = []
secondary_target = []
secondary_non_code = []
secondary_code = []
for line in Secondary_lines:
	line = line.split()
	print(line[2])
	secondary_target.append(int(line[1]))
	secondary_training.append([int(line[2])])
	if line[1] == 0:
		secondary_non_code.append(int(line[2]))
	else:
		secondary_code.append(int(line[2]))
ATG_training = []
ATG_target = []
ATG_non_code = []
ATG_code = []
for line in ATG_lines:
	line = line.split()
	print(line[2])
	ATG_target.append(int(line[1]))
	ATG_training.append([int(line[2])])
	if line[1] == 0:
		ATG_non_code.append(int(line[2]))
		print(line[2])
	else:
		ATG_code.append(int(line[2]))
print('ATG_Conservation')
print('Coding_Sequences')
print(sum(ATG_code)/float(len(ATG_code)))
print(numpy.std(ATG_code))
print('Non_Coding_Sequences')
print(sum(ATG_non_code)/float(len(ATG_non_code)))
print(numpy.std(ATG_non_code))
clf = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
score = cross_validation.cross_val_score(clf, ATG_training, ATG_target, cv = 5)
print(score.mean())
print(score.std())

print('Secondary_Structure')
print('Coding_Sequences')
print(sum(secondary_code)/float(len(secondary_code)))
print(numpy.std(secondary_code))
print('Non_Coding_Sequences')
print(sum(secondary_non_code)/float(len(secondary_non_code)))
print(numpy.std(secondary_non_code))
clf2 = RandomForestClassifier(n_estimators = 100, min_samples_split = 1)
score = cross_validation.cross_val_score(clf2, secondary_training, secondary_target, cv = 5)
print(score.mean())
print(score.std())


