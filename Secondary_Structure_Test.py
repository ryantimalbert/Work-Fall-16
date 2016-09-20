import MySQLdb as SQL
import sys
import subprocess
def test_secondary(database):
	connect = SQL.connect("gpdb02", "rtalbert", "Spike123@@", database)
	cursor = connect.cursor()
	cursor.execute("select distinct id from fgenesh1_kg limit 10;")
	featureIds = cursor.fetchall()
	# bash = open('secondary_calc_bash.sh', 'w+')
	# bash.write('#!/bin/bash\n')
	# bash.write('module load EMBOSS/6.4.0\n')
	# bash.write('garnier protein_sequence.txt secondary_protein_out')
	for featureId in featureIds:
		file = open('protein_sequence.txt', 'w+')
		featureId = featureId[0]
		cursor.execute("select id from featureLink where featureId = {featureIdVal} and featureTable = 'fgenesh1_kg' and type like 'transcript%';". format(featureIdVal = featureId))
		transcriptId = cursor.fetchone()[0]
		cursor.execute("select seq from protein where transcriptId = {Id};".format(Id = transcriptId))
		sequence = cursor.fetchone()[0]
		file.write(sequence[0 : -1] + '\n')
		cursor.execute("select id from featureLink where featureId = {featureIdVal} and featureTable = 'fgenesh1_kg' and type like 'protein%';". format(featureIdVal = featureId))
		proteinId = cursor.fetchone()[0]
		cursor.execute("select count(*) from proteinSW where proteinId = {proteinIdVal};".format(proteinIdVal = proteinId))
		if cursor.fetchone()[0] == 0:
			code_bool_val = 0
		else:
			code_bool_val = 1
		print(code_bool_val)
		file.close()
		subprocess.call("module load EMBOSS/6.4.0", shell = True)
		subprocess.call('garnier protein_sequence.txt secondary_protein_out', shell = True)
		data_file = open('secondary_protein_out', 'r')
		data_file_line = data_file.readlines()
		H_value = 0
		E_value = 0
		length_sequence = 0
		for data in data_file_line:
			data = data.split()
			if 'Residue' in data:
				num = 0
				print(data)
				if len(data[3]) > 2:
					H = data[3]
					digit_length = len(H)
					H_value = int(H[2 : digit_length])
					num = 4
				else:
					H_value = int(data[4])
					num = 5
				if len(data[num]) > 2:
					E = data[num]
					digit_length = len(E)
					H_value = int(E[2 : digit_length])
				else:
					E_value = int(data[num + 1])
			if 'Total_length:' in data:
				length_sequence = int(data[2])
		print(float(H_value + E_value)/ length_sequence)
database = sys.argv[1]
test_secondary(database)