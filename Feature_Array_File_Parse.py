
from CodingPotentialFeature import CodingPotentialFeatureCalc
def compile_feature_list(transcript_file, blast_file, database):
	transcript_file = open('ModelDataFiles/' + transcript_file, 'r')
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
	blast_file = open('ModelDataFiles/' + blast_file, 'r')
	blast_file = blast_file.readlines()
	feature_codes = {}
	for line in blast_file:
		line = line.split()
		code_bool = 0
		if len(line) > 1:
			code_bool = 1
		line = line[0]
		dash_count = 0
		gene_code = ""
		count = 0
		while dash_count < 5:
			gene_code += line[count]
			count += 1
			if line[count] == '_':
				dash_count += 1
		count += 2
		start = ""
		while line[count] != '_':
			start += line[count]
			count += 1
		count += 2
		end = ""
		while line[count] != '_':
			end += line[count]
			count += 1
		count +=2
		pos_or_neg = line[count]
		start = int(start)
		end = int(end)
		active_dictionary = gene_codes[gene_code]
		feature_codes[gene_code] = active_dictionary
		active_dictionary['code_boolean'] = code_bool
		sequence = active_dictionary['transcript'].lower()
		cds_seq = ""

		ATG_Conservation_Val = 0
		if pos_or_neg == "+":
			cds_seq = sequence[start - 1: end]
			# if (start - 16) >= 0 and (start + 14) <= len(sequence):
			# 	conservation_sequence = sequence[(start - 16) : (start + 14)]
			# 	for nucleo in conservation_sequence:
			# 		if nucleo.lower() == "a":
			# 			ATG_Conservation_Val += A_Value
			# 		elif nucleo.lower() == "g":
			# 			ATG_Conservation_Val += G_Value
			# 		elif nucleo.lower() == "t":
			# 			ATG_Conservation_Val += T_Value
			# 		elif nucleo.lower() == "c":
			# 			ATG_Conservation_Val += C_Value
			# 		else:
			# 			pass

		else:
			### ATG Start Conservation feature
			# if ((start - 1) - 15) >= 0 and ((start - 1) + 15) <= len(sequence):
			# 	count = start + 14
			# 	while count >= (start - 16):
			# 		nucleo = sequence[count]
			# 		if nucleo.lower() == "a":
			# 			ATG_Conservation_Val += T_Value
			# 		elif nucleo.lower() == "g":
			# 			ATG_Conservation_Val += C_Value
			# 		elif nucleo.lower() == "t":
			# 			ATG_Conservation_Val += A_Value
			# 		elif nucleo.lower() == "c":
			# 			ATG_Conservation_Val += G_Value
			# 		else:
			# 			pass
			# 		count -= 1

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
	for key_name in feature_codes.keys():
		count += 1
		current_vector = []
		current_vector.append(feature_codes[key_name]['lens_length'])
		current_vector.append(feature_codes[key_name]['lens_ratio'])
		current_vector.append(CodingPotentialFeatureCalc(feature_codes[key_name]['cds'], database))
		# current_vector.append(ATG_Conservation_Val)
		training_vectors.append(current_vector)
		target_values.append(feature_codes[key_name]['code_boolean'])
	return(training_vectors, target_values)

def compile_feature_list2(transcript_file, blast_file, database):
	transcript_file = open('ModelDataFiles/' + transcript_file, 'r')
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
	blast_file = open('ModelDataFiles/' + blast_file, 'r')
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
	for key_name in feature_codes.keys():
		count += 1
		current_vector = []
		current_vector.append(feature_codes[key_name]['lens_length'])
		current_vector.append(feature_codes[key_name]['lens_ratio'])
		current_vector.append(CodingPotentialFeatureCalc(feature_codes[key_name]['cds'], database))
		training_vectors.append(current_vector)
		target_values.append(feature_codes[key_name]['code_boolean'])
	return(training_vectors, target_values)

