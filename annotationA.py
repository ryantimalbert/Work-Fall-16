#! /usr/bin/python

from Bio import SeqIO
from Bio import pairwise2
import sys


try:
    seq_fileA,seq_fileB= str(sys.argv[1]),str(sys.argv[2])
except:
    raise AttributeError("Incorrect Arguments!")

fasta_A = [fasta for fasta in SeqIO.parse(seq_fileA,"fasta")]
fasta_B = [fasta for fasta in SeqIO.parse(seq_fileB,"fasta")]

Information_file=open("Information File_aeuroginosa.fna","w")
def comparison(ref_seq,comparison_genome):
    bucket = len(ref_seq.seq)
    window = 50
    scores=[]
    for comp_seq in comparison_genome:
        score=-9999999
        comp_seq_len = len(comp_seq)
        #sets the minimum threshold
        print "comparing: " + ref_seq.id + comp_seq.id
        if bucket<comp_seq_len:
            threshold = 0
            #.5*bucket
        else:
            threshold = 0
            #.5*comp_seq_len
        #compares the two sequences
        if bucket<=(comp_seq_len + window) and bucket>=(comp_seq_len - window):
            score = pairwise2.align.globalms(ref_seq.seq,comp_seq.seq,2,-3,-5,-2,score_only=True)
            if score >= threshold:
                print(score)
                return True
            else:
                scores.append(score)

    Information_file.write("Comparing "+ref_seq.id + " | " +comp_seq.id+'\n')
    #Information_file.write("Max Score:" + str(max(scores))+'\n')
    return False

fasta_found,id_found=[],[]
fasta_missing, id_missing=[],[]
for sequence in fasta_A:
    if not comparison(sequence,fasta_B):
        fasta_missing.append(sequence)
        id_missing.append(sequence.id)
    else:
        fasta_found.append(sequence)
        id_found.append(sequence.id)
        #print sequence.id + " is missing"

id_file1=open("Missing_Genes_aeuroginosa.id.fna","w")
for sequence in id_missing:
    id_file1.write(sequence+'\n')
SeqIO.write(fasta_missing, "Missing_Genes_aeuroginosa.cds.fna", "fasta")
id_file2=open("Found_Genes_aeuroginosa.id.fna","w")
for sequence in id_found:
    id_file2.write(sequence+'\n')
SeqIO.write(fasta_found, "Found_Genes_aeuroginosa.cds.fna", "fasta")
