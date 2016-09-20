import MySQLdb as SQL
import time
import sys
from math import log

def compilation(connection, table):
	cursor1 = connection.cursor()
	codingSequence = ""
	non_codingSequence = ""
	cursor1.execute("select id from {table1};".format(table1 = table))
	featureId = cursor1.fetchall()
	for singleId in featureId:
		# current_time = time.time()
		# if current_time - time0 > 800:
		# 	error_file = open('Too_Long/{database}.txt'.format(database = name), 'wb')
		# 	error_file.close()
		# 	return None
		cursor1.execute("select id from featureLink where featureId = {checkId} and featureTable = '{table2}' and type like 'transcript%';".format(checkId = singleId[0], table2 = table))
		transcriptId = cursor1.fetchone()
		if transcriptId == None:
			continue;
		transcriptId = transcriptId[0]
		cursor1.execute("select seqCDS from transcript where transcriptId = {checkTranscript};".format(checkTranscript = transcriptId))
		initial_sequence = cursor1.fetchone()
		if initial_sequence == None:
			continue;
		initial_sequence = initial_sequence[0]
		if initial_sequence[0:3].lower() == "atg":
			codingSequence += initial_sequence
	cursor1.execute("select chrom, start, end, cdsStart, cdsEnd from {table3};".format(table3 = table))
	query = cursor1.fetchall()
	index = 0
	prev_scaffold = ""
	total_runs = 0
	for row in query:
		# current_time = time.time()
		# if current_time - time0 > 800:
		# 	error_file = open('Too_Long/{database}.txt'.format(database = name), 'wb')
		# 	error_file.close()
		# 	return None
	    scaffold = row[0]
	    start = row[1]
	    end = row[2]
	    cdsStart = row[3]
	    cdsEnd = row[4]
	    cdsStart1 = cdsStart -1
	    if prev_scaffold != scaffold and prev_scaffold != "":
	    	cursor1.execute("select seq from scaffoldSeq where scaffold = '{chromosome}'".format(chromosome = prev_scaffold))
	    	scaffSequence = cursor1.fetchone()[0]
	    	non_codingSequence += scaffSequence[index : len(scaffSequence)]
	    	index = 0
	    cursor1.execute("select seq from scaffoldSeq where scaffold = '{chromosome}'".format(chromosome = scaffold))
	    scaffSequence = cursor1.fetchone()[0]
	    non_codingSequence += scaffSequence[index : (start - 1)]
	    if start != cdsStart:
	    	non_codingSequence += scaffSequence[(start - 1) : (cdsStart - 1)]
	    if end != cdsEnd:
	    	non_codingSequence += scaffSequence[cdsEnd : end]

	    prev_scaffold = scaffold
	    index = end
	    ## Compiling conservation around ATG start codon
	  #   nucleo_counts = {}
	  #   nucleotides = ['a', 'g', 'c', 't']
	  #   for i in range(-5 , 6):
	  #   	for nucleo in nucleotides:
			# nucleo_counts[nucleo + str(i)] = 0
	  #   if scaffSequence[cdsStart1 : cdsStart1 + 3].lower() == "atg" and (cdsStart1 - 5) >= 0 and (cdsStart1 + 6) <= len(scaffSequence):
	  #   	conservation_sequence = scaffSequence[(cdsStart1 - 5) : (cdsStart1 + 6)]
	  #   	count = -5
	  #   	for nucleo in conservation_sequence:
	  #   		if nucleo.lower() == "a":
	  #   			nucleo_counts['a' + str(count)] += 1
	  #   		elif nucleo.lower() == "g":
	  #   			nucleo_counts['g' + str(count)] += 1
	  #   		elif nucleo.lower() == "t":
	  #   			nucleo_counts['t' + str(count)] += 1
	  #   		elif nucleo.lower() == "c":
	  #   			nucleo_counts['c' + str(count)] += 1
	  #   		else:
	  #   			pass
	  #   		count += 1
	  #   total_runs += 1
	cursor1.close()

	### Conservation around ATG start Codon

	# file = open('ATG_Conservation/{database}.txt'.format(database = name), 'w+')
	# file_read = open('Total_Breakdown/{database}.txt'.format(database = name), 'r')
	# reading = file_read.readlines()
	# for line in reading:
	# 	line = line.split()
	# 	total_percentage = float(line[1])
	# 	if line[0] == "A":
	# 		for i in range(-5 , 6):
	# 			current_percent = float(nucleo_counts['a' + str(i)]) / total_runs
	# 			divided_num = current_percent / total_percentage
	# 			value = int(log(divided_num, 2) * 100)
	# 			file.write('A{num} {conservation_val}\n'.format(num = i, conservation_val = value))
	# 	elif line[0] == "G":
	# 		for i in range(-5 , 6):
	# 			current_percent = float(nucleo_counts['g' + str(i)]) / total_runs
	# 			divided_num = current_percent / total_percentage
	# 			value = int(log(divided_num, 2) * 100)
	# 			file.write('G{num} {conservation_val}\n'.format(num = i, conservation_val = value))
	# 	elif line[0] == "T":
	# 		for i in range(-5 , 6):
	# 			current_percent = float(nucleo_counts['t' + str(i)]) / total_runs
	# 			divided_num = current_percent / total_percentage
	# 			value = int(log(divided_num, 2) * 100)
	# 			file.write('T{num} {conservation_val}\n'.format(num = i, conservation_val = value))
	# 	else:
	# 		for i in range(-5 , 6):
	# 			current_percent = float(nucleo_counts['c' + str(i)]) / total_runs
	# 			divided_num = current_percent / total_percentage
	# 			value = int(log(divided_num, 2) * 100)
	# 			file.write('C{num} {conservation_val}\n'.format(num = i, conservation_val = value))
	# file_read.close()
	# file.close()
	return (codingSequence, non_codingSequence)

def calculation(transcripts):
	coding_permutations = {}
	non_coding_permutations = {}
	options = ['a','t','c','g']
	for first in options:
		for second in options:
			for third in options:
				for fourth in options:
					for fifth in options:
						for sixth in options:
							coding_permutations[first + second + third + fourth + fifth + sixth + str(1)] = 0
							coding_permutations[first + second + third + fourth + fifth + sixth + str(2)] = 0
							coding_permutations[first + second + third + fourth + fifth + sixth + str(3)] = 0
							non_coding_permutations[first + second + third + fourth + fifth + sixth] = 0
	coding = transcripts[0]
	non_coding = transcripts[1]
	count = 0
	subscripts = [1,2,3] ### used to get coding potential value for position 1,2 or 3
	subscriptCount = 0
	while count <= len(coding) - 6:
		hexomer = coding[count : count + 6].lower() + str(subscripts[subscriptCount])
		if 'n' in hexomer: ## does not factor in hexomers that include an unknown
			pass
		else:
			coding_permutations[hexomer] += 1
		if subscriptCount == 2: ## increments knowledge of the 1,2, or 3 position 
			subscriptCount = 0
		else:
			subscriptCount += 1
		count += 1
	count = 0
	while count <= len(non_coding) - 6:
		hexomer = non_coding[count : count + 6].lower()
		if 'n' in hexomer: ## does not factor in hexomers that include an unknown
			pass
		else:
			non_coding_permutations[hexomer] += 1
		count += 1
	return(coding_permutations, non_coding_permutations)

name = sys.argv[1]
table = sys.argv[2]
connect= SQL.connect("gpdb02", "rtalbert", "Spike123@@", name)
time0 = time.time()
print('==============================================================')
print(name)
print('Coding Potential Compilation Started')
compiled_transcripts = compilation(connect, table)
coding_length = len(compiled_transcripts[0])
non_coding_length = len(compiled_transcripts[1])
connect.close()
time1 = time.time()
print(name)
print('====================================================================')
print("Compilation time: {clock} ".format(clock = str(time1 - time0)))
time0 = time.time()
Coding_Potential_Values = calculation(compiled_transcripts)
time1 = time.time()
print(name)
print('======================================================================')
print("Calculation time: {clock} ".format(clock = str(time1 - time0)))
file = open('Coding_Potential_Files/{database}.txt'.format(database = name), 'w+')
coding_map = Coding_Potential_Values[0]
non_coding_map = Coding_Potential_Values[1]
for value in non_coding_map.keys():
	for num in range(1,4):
		coding_value = coding_map[value + str(num)]
		non_coding_value = non_coding_map[value]
		if coding_value == 0 or non_coding_value == 0:
			coding_value += 1
			non_coding_value += 1
		elif non_coding_value >= 3:
			non_coding_value = non_coding_value/3
		coding_value = float(coding_value)/coding_length
		non_coding_value = float(non_coding_value)/non_coding_length
		divided_num = coding_value/non_coding_value
		# divided_num = (float(coding_value)/ coding_length) / (float(non_coding_value)/ non_coding_length) ## length normalized calculation
		coding_potential_value = int(log(divided_num, 2) * 10) ### could try rounding instead more precision
		file.write("{hex} : {potential}\n".format(hex = value + str(num), potential = str(coding_potential_value)))

