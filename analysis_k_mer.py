import sys
from math import log
fasta = sys.argv[1]
k_mer = int(sys.argv[2])
file1 = open(fasta, 'r')
lines = file1.readlines()
sequence = ""
for line in lines:
	if '>' not in line:
		line = line.replace('\n', '')
		sequence += line
sequence = sequence.upper()
nucleotides = ['A','T','C','G']
amino = {}
amino['R'] = 'CGA'
amino['K'] = 'AAA'
amino['Y'] = 'TAT'
amino['M'] = 'ATG'
amino['W'] = 'TGG'
new_seq = ''
for i in sequence:
	if i not in nucleotides:
		new_seq += amino[i]
	else:
		new_seq += i
counts = {}
def permutations(n, string = ''):
	if n == 0:
		for i in range(1,4):
			counts[string + str(i)] = 0
	else:
		for i in nucleotides:
			string1 = string[:]
			string1 += i
			permutations(n - 1, string1)
permutations(k_mer)
non_code_counts = {}
for i in counts:
	non_code_counts[i] = 0





list_of_frames1 = []
list_of_frames2 = []
list_of_frames3 = []

glimmer = sys.argv[3]
orf_file = open(glimmer, 'r')
lines = orf_file.readlines()
for line in lines:
	line = line.split()
	if len(line) == 0:
		continue;
	if 'orf' in line[0]:
		if line[3] == '+1':
			list_of_frames1.append((int(line[1]), int(line[2])))
		elif line[3] == '+2':
			list_of_frames2.append((int(line[1]), int(line[2])))
		elif line[3] == '+3':
			list_of_frames3.append((int(line[1]), int(line[2])))
		else:
			pass
	else:
		pass


list_of_sections = []
conglomerate_non_code = ""
last = 0
for i in list_of_frames1:
	conglomerate_non_code += new_seq[last : i[0] - 1]
	list_of_sections.append(new_seq[i[0] - 1 : i[1]])
	last = i[1]
conglomerate_non_code += new_seq[last : len(new_seq)]
count = 0
first_read_length = len(conglomerate_non_code)
while (count + k_mer) <= len(conglomerate_non_code):
	k = conglomerate_non_code[count : count + k_mer]
	non_code_counts[k + str(1)] += 1
	count += k_mer
first_code_length = 0
for i in list_of_sections:
	first_code_length += len(i)
	count = 0
	while count + k_mer <= len(i):
		k = i[count : count + k_mer]
		counts[k + str(1)] += 1
		count += k_mer



list_of_sections = []
conglomerate_non_code = ""
last = 0
for i in list_of_frames2:
	conglomerate_non_code += new_seq[last : i[0] - 1]
	list_of_sections.append(new_seq[i[0] - 1 : i[1]])
	last = i[1]
conglomerate_non_code += new_seq[last : len(new_seq)]
count = 0
second_read_length = len(conglomerate_non_code)
while (count + k_mer) <= len(conglomerate_non_code):
	k = conglomerate_non_code[count : count + k_mer]
	non_code_counts[k + str(2)] += 1
	count += k_mer
second_code_length = 0
for i in list_of_sections:
	second_code_length += len(i)
	count = 1
	while count + k_mer <= len(i):
		k = i[count : count + k_mer]
		counts[k + str(2)] += 1
		count += k_mer

list_of_sections = []
conglomerate_non_code = ""
last = 0
for i in list_of_frames3:
	conglomerate_non_code += new_seq[last : i[0] - 1]
	list_of_sections.append(new_seq[i[0] - 1 : i[1]])
	last = i[1]
conglomerate_non_code += new_seq[last : len(new_seq)]
count = 0
third_read_length = len(conglomerate_non_code)
while (count + k_mer) <= len(conglomerate_non_code):
	k = conglomerate_non_code[count : count + k_mer]
	non_code_counts[k + str(3)] += 1
	count += k_mer
third_code_length = 0
for i in list_of_sections:
	third_code_length += len(i)
	count = 2
	while count + k_mer <= len(i):
		k = i[count : count + k_mer]
		counts[k + str(3)] += 1
		count += k_mer

out_file = open('coding_potential', 'w+')
for i in counts:
	length_coding = 0
	length_not_coding = 0
	if i[6] == '1':
		length_coding = first_code_length
		length_not_coding = first_read_length
	elif i[6] == '2':
		length_coding = second_code_length
		length_not_coding = second_read_length
	elif i[6] == '3':
		length_coding = third_code_length
		length_not_coding = third_read_length
	else:
		print('here')
	coding_ratio = float(counts[i]) / length_coding
	non_coding_ratio = float(non_code_counts[i]) / length_not_coding
	total_ratio = coding_ratio/non_coding_ratio
	if total_ratio == 0:
		potential = 0
	else:
		potential = log(total_ratio, 2)
	out_file.write('{hexomer} {num} \n '.format(hexomer = i, num = potential * 100))
out_file.close()


# total_k_mers = 0
# for frame in range(3):
# 	count = frame
# 	while count + k_mer <= len(new_seq):
# 		k = new_seq[count : count + k_mer]
# 		total_k_mers += 1
# 		counts[k + str(frame + 1)] += 1
# 		count += k_mer
# per_frame = total_k_mers/3
# out_file = open('{num}_mer_counts.txt'.format(num = k_mer), 'w+')
# for i in counts:
# 	out_file.write('{mer} : {val} '.format(mer = i, val = counts[i]) + '\n')
# out_file.close()




# next_outfile = open('{num}_mer_repeats.txt'.format(num = k_mer), 'w+')
# count = 0
# up_to = 0
# found = False
# values = []
# searching = ""
# seen = 0
# while count + k_mer <= len(new_seq):
# 	if found:
# 		if up_to + k_mer >= 1000:
# 			up_to = 0
# 			found = False
# 			values.append([searching, seen])
# 			seen = 0
# 			searching = ""
# 		else:
# 			mer = new_seq[count : count + k_mer]
# 			if mer == searching:
# 				seen += 1
# 			count += k_mer
# 			up_to += k_mer
# 	else:
# 		start = new_seq[count : count + 3]
# 		count += 3
# 		if start == 'ATG':
# 			found = True
# 			searching = new_seq[count : count + k_mer]
# 			count += k_mer
# for i in values:
# 	next_outfile.write('{mer} : {val} '.format(mer = i[0], val = i[1]) + '\n')
# 	if i[1] > 0:
# 		print(i[0])
# 		print(i[1])
# next_outfile.close()


