import MySQLdb as SQL
import sys
import subprocess
def compile_feature_list2(transcript_file, blast_file, database):
	transcript_file = open(transcript_file, 'r')
	transcript_file = transcript_file.readlines()
	gene_codes = {}
	gene_code = ""
	sequence = ""
	for line in transcript_file:
		if line[0] == ">":
			if gene_code != "":
				data= {}
				gene_codes[gene_code] = data
				data['transcript'] = sequence
			line = line.split()
			gene_code = line[0]
			sequence = ""
		else:
			sequence += line[0 : -1]
	data= {}
	gene_codes[gene_code] = data
	data['transcript'] = sequence
	blast_file = open(blast_file, 'r')
	blast_file = blast_file.readlines()
	feature_codes = {}
	for line in blast_file:
		line = line.split()
		code_bool = 0
		if len(line) > 1: ## Can tell if multiploe words, if there is then its protein coding
			code_bool = 1
		line = line[0]
		gene_code = ""
		count = 0
		while line[count] != '_': ## compiling gene type
			gene_code += line[count]
			count += 1
		if line[count + 1] ==  'P':
			gene_code += line[count]
			count +=1
			while line[count] != '_':
				gene_code += line[count]
				count +=1 
		count += 2
		start = ""
		while line[count] != '_': ## getting start position
			start += line[count]
			count += 1
		count +=2
		end = ""
		while line[count] != '_': ## getting end position
			end +=  line[count]
			count +=1 
		count += 2
		pos_or_neg = line[count]
		start = int(start)
		end = int(end)
		active_dictionary = gene_codes[gene_code]
		feature_codes[gene_code] = active_dictionary
		active_dictionary['code_boolean'] = code_bool
		sequence = active_dictionary['transcript'].lower()
		cds_seq = ""
		if pos_or_neg == "+":
			cds_seq = sequence[start - 1: end]
		else:
			count = end - 1
			while count >= (start - 1):
				nucleotide = sequence[count]
				if nucleotide == "n":
					cds_seq += nucleotide
				elif nucleotide == "a":
					cds_seq += "t"
				elif nucleotide == "t":
					cds_seq += "a"
				elif nucleotide == "c":
					cds_seq += "g"
				else:
					cds_seq += "c"
				count -= 1
		active_dictionary['cds'] = cds_seq
		active_dictionary['lens_length'] = len(cds_seq)
		active_dictionary['lens_ratio'] = float(len(cds_seq))/len(sequence)
		active_dictionary['transcript'] = sequence
	training_vectors = []
	target_values = []
	result = []
	for key_name in feature_codes.keys():
		internal = []
		internal.append(feature_codes[key_name]['cds'])
		internal.append(feature_codes[key_name]['code_boolean'])
		internal.append(key_name)
		result.append(internal)
	return result
def test_secondary(database, fasta, blast):
	featureIds = compile_feature_list2(fasta, blast, database)
	out_put = open('secondary_out.txt', 'w+')
	for Id in featureIds:
		file = open('protein_sequence.txt', 'w+')
		file.write(Id[0])
		file.close()
		coding = Id[1]
		tag = Id[2]
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
		out_put.write(tag + " " + str(coding) + " " + str(float(H_value + E_value)/ length_sequence) + '\n')
	out_put.close()
database = sys.argv[1]
fasta = sys.argv[2]
blast = sys.argv[1]
test_secondary(database, fasta, blast)