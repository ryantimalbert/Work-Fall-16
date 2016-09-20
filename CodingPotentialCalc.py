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


	    # Compiling conservation around ATG start codon
	    nucleo_counts = {}
	    nucleotides = ['a', 'g', 'c', 't']
	    for i in range(-10 , 10):
	    	for nucleo in nucleotides:
			nucleo_counts[nucleo + str(i)] = 0
	    if scaffSequence[cdsStart1 : cdsStart1 + 3].lower() == "atg" and (cdsStart1 - 5) >= 0 and (cdsStart1 + 6) <= len(scaffSequence):
	    	conservation_sequence = scaffSequence[(cdsStart1 - 5) : (cdsStart1 + 6)]
	    	count = -5
	    	for nucleo in conservation_sequence:
	    		if nucleo.lower() == "a":
	    			nucleo_counts['a' + str(count)] += 1
	    		elif nucleo.lower() == "g":
	    			nucleo_counts['g' + str(count)] += 1
	    		elif nucleo.lower() == "t":
	    			nucleo_counts['t' + str(count)] += 1
	    		elif nucleo.lower() == "c":
	    			nucleo_counts['c' + str(count)] += 1
	    		else:
	    			pass
	    		count += 1
	    total_runs += 1
	    print(total_runs)

	cursor1.close()

	## Conservation around ATG start Codon

	file = open('ATG_Conservation/{database}.txt'.format(database = name), 'w+')
	file_read = open('Total_Breakdown/{database}.txt'.format(database = name), 'r')
	reading = file_read.readlines()
	for line in reading:
		line = line.split()
		total_percentage = float(line[1])
		if line[0] == "A":
			for i in range(-10 , 10):
				current_percent = float(nucleo_counts['a' + str(i)]) / total_runs
				divided_num = current_percent / total_percentage
				value = int(log(divided_num, 2) * 100)
				file.write('A{num} {conservation_val}\n'.format(num = i, conservation_val = value))
		elif line[0] == "G":
			for i in range(-10 , 10):
				current_percent = float(nucleo_counts['g' + str(i)]) / total_runs
				divided_num = current_percent / total_percentage
				value = int(log(divided_num, 2) * 100)
				file.write('G{num} {conservation_val}\n'.format(num = i, conservation_val = value))
		elif line[0] == "T":
			for i in range(-10 , 10):
				current_percent = float(nucleo_counts['t' + str(i)]) / total_runs
				divided_num = current_percent / total_percentage
				value = int(log(divided_num, 2) * 100)
				file.write('T{num} {conservation_val}\n'.format(num = i, conservation_val = value))
		else:
			for i in range(-10 , 10):
				current_percent = float(nucleo_counts['c' + str(i)]) / total_runs
				divided_num = current_percent / total_percentage
				value = int(log(divided_num, 2) * 100)
				file.write('C{num} {conservation_val}\n'.format(num = i, conservation_val = value))
	file_read.close()
	file.close()
	return (codingSequence, non_codingSequence)
name = sys.argv[1]
table = sys.argv[2]
connect= SQL.connect("gpdb05", "asalamov", "asalamov", name)
compilation(connect, table)

