import sys
def compile_feature_list(transcript_file, blast_file, database):
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
	file = open('ATG_Conservation/{database}.txt'.format(database = database), 'r')
	lines = file.readlines()
	ATG_Con_Index = {}
	out_file = open('ATG_Con_Out_Neucr2', 'wb')
	for line in lines:
		line = line.split()
		ATG_Con_Index[line[0]] = int(line[1])
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
			if (start - 11) >= 0 and ((start - 1) + 9) < len(sequence):
				count = -10
				while (start - 1) + count <= (start - 1) + 9:
					nucleo = sequence[(start - 1) + count]
					if nucleo.lower() == "a":
						ATG_Conservation_Val += ATG_Con_Index['A' + str(count)]
					elif nucleo.lower() == "g":
						ATG_Conservation_Val += ATG_Con_Index['G' + str(count)]
					elif nucleo.lower() == "t":
						ATG_Conservation_Val += ATG_Con_Index['T' + str(count)]
					elif nucleo.lower() == "c":
						ATG_Conservation_Val += ATG_Con_Index['C' + str(count)]
					else:
						pass
					count += 1

		else:
			### ATG Start Conservation feature
			if ((start - 1) - 10) >= 0 and ((start - 1) + 9) < len(sequence):
				count = 9
				while (start - 1) + count >= (start - 11):
					nucleo = sequence[(start - 1) + count]
					if nucleo.lower() == "a":
						ATG_Conservation_Val += ATG_Con_Index['T' + str(count)]
					elif nucleo.lower() == "g":
						ATG_Conservation_Val += ATG_Con_Index['C' + str(count)]
					elif nucleo.lower() == "t":
						ATG_Conservation_Val += ATG_Con_Index['A' + str(count)]
					elif nucleo.lower() == "c":
						ATG_Conservation_Val += ATG_Con_Index['G' + str(count)]
					else:
						pass
					count -= 1
		out_file.write(str(gene_code) + ' ' + str(code_bool) + ' ' + str(ATG_Conservation_Val))
	out_file.close()
database = sys.argv[1]
fasta = sys.argv[2]
blast = sys.argv[3]
compile_feature_list(fasta, blast, database)

