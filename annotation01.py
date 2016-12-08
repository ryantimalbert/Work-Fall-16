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
Information_fileA=open("Missing Genes.aeuroginosa.fna","w")
Information_fileB=open("Found Genes.aeuroginosa.fna","w")
def comparison(ref_seq,comparison_genome):

    scores=[]
    for comp_seq in comparison_genome:
        #sets the minimum threshold
        print "comparing: " + ref_seq.id +" with "+ comp_seq.id
        if len(ref_seq.seq)<len(comp_seq.seq):
            threshold = .5*len(ref_seq.seq)
        else:
            threshold = .5*len(comp_seq.seq)
        #compares the two sequences
        score = pairwise2.align.globalms(ref_seq.seq,comp_seq.seq,2,-3,-5,-2,score_only=True)
        scores.append(score)
        #print(score,threshold)
        if score >= threshold:
            Information_fileB.write("Comparing "+ref_seq.id+'\n')
            Information_fileB.write("Score is "+str(score)+'\n'+"Threshold is "+str(threshold)+'\n')
            return True
    #print(max(scores))
    Information_fileA.write("Comparing "+ref_seq.id+'\n')
    Information_fileA.write("Max Score: " + str(max(scores))+'\n'+"Threshold "+str(threshold)+'\n')
    return False


fasta_output,id_output=[],[]
for sequence in fasta_A:
    if not comparison(sequence,fasta_B):
        fasta_output.append(sequence)
        id_output.append(sequence.id)
        #print sequence.id + " is missing"

id_file=open("Annotation ID.aeuroginosa.fna","w")
for sequence in id_output:
    id_file.write(sequence+'\n')
SeqIO.write(fasta_output, "Annotation Output.aeuroginosa.fna", "fasta")
