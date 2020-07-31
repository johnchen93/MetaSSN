#!python3
import helper
import argparse
import os

def get_length(file, label):
    seqs = helper.ReadFasta(file)
    lens = {}
    for header, seq in seqs.items():
        lens[header] = len(seq)
    print(min(lens.values()), max(lens.values()))
    out = {}
    with open(f"{label}",'w') as f:
        for header, length in lens.items():
            f.write(f"{header}\t{length}\n")

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Determine the lengeth of each sequence in a fasta file.")
    parser.add_argument('infile', metavar='i', type=str, help='Input fasta file.')
    parser.add_argument('outlabel', metavar='o', type=str, help='Name for the filtered fasta.')
    args = parser.parse_args()
    
    get_length(args.infile, args.outlabel)