import MySQLdb as SQL
import time
import sys
def Compile_Transcript(connection):
	cursor = connection.cursor()
	cursor.execute("Select seqTranscript from transcript;")
	total_transcript = ""
	for transcript in cursor.fetchall():
		total_transcript += transcript[0]
	cursor.close()
	connection.close()
	return total_transcript
def total_breakdown(transcript):
	A_count = 0
	C_count = 0
	G_count = 0
	T_count =  0
	for nucleo in transcript:
		if nucleo.lower() == "a":
			A_count += 1
		elif nucleo.lower() == "g":
			G_count += 1
		elif nucleo.lower() == "t":
			T_count  += 1
		elif nucleo.lower() == "c":
			C_count += 1
		else:
			pass
	file = open('Total_Breakdown/{database}.txt'.format(database = name), 'w+')
	total = A_count + T_count + C_count + G_count
	A_number = float(A_count)/ total
	file.write('A {num}\n'.format(num = A_number))
	G_number = float(G_count)/ total
	file.write('G {num}\n'.format(num = G_number))
	T_number = float(T_count)/ total
	file.write('T {num}\n'.format(num = T_number))
	C_number = float(C_count)/ total
	file.write('C {num}\n'.format(num = C_number))
	file.close()

name = sys.argv[1]
connect= SQL.connect("gpdb05", "asalamov", "asalamov", name)
transcript_con = Compile_Transcript(connect)
total_breakdown(transcript_con) ## Used for conservation around ATG
file = open('GC_Content_File.txt', 'a')
file.write("{database} GC Content: {value}%\n".format(database = name, value = str(GC)))