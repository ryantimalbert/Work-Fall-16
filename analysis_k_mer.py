import sys
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
total_k_mers = 0
for frame in range(3):
	count = frame
	while count + k_mer <= len(new_seq):
		k = new_seq[count : count + k_mer]
		total_k_mers += 1
		counts[k + str(frame + 1)] += 1
		count += k_mer
per_frame = total_k_mers/3
out_file = open('{num}_mer_counts.txt'.format(num = k_mer), 'w+')
for i in counts:
	out_file.write('{mer} : {val} '.format(mer = i, val = counts[i]) + '\n')
out_file.close()


