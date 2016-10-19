import sys
from sklearn.ensemble import ExtraTreesClassifier
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
count = 0
checked_genomes = []
for line in lines[1::]:
	line = line.split()
	genome = line[0]
	if genome == '##OUTGROUP':
		continue;
	if 'saprophyte' in line or 'saprophytic' in line:
		Genomes[genome].append(1)
		checked_genomes.append(genome)
	else:
		Genomes[genome].append(0)
		checked_genomes.append(genome)
target = []
features = []
for genome in Genomes:
	if genome in checked_genomes:
		target.append(Genomes[genome][1])
		features.append(Genomes[genome][0])
clf = ExtraTreesClassifier()
clf = clf.fit(features, target)
weight_array = clf.feature_importances_
valued_p_fam = []
count = 0
PFAM = PFAM_Parse[1 ::]
for num in weight_array:
	if num != 0:
	    valued_p_fam.append(PFAM_Parse[count][0])	
	count += 1	
print(valued_p_fam)
print(len(valued_p_fam))


