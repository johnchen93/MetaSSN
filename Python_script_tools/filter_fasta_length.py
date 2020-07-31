#!python3
import helper
import argparse
import os

def merge(file, minlen, maxlen, label):
    seqs = helper.ReadFasta(file)
    lens = {}
    for header, seq in seqs.items():
        lens[header] = len(seq)
    print(min(lens.values()), max(lens.values()))
    out = {}
    with open(f"{label}_{minlen}-{maxlen}aa_excluded.txt",'w') as f:
        for header, length in lens.items():
            if length >=minlen and length <=maxlen:
                out[header] = seqs[header]
            else:
                f.write(f"{header}\t{length}\n")
                print(header, length)
    helper.WriteFasta(out, f"{label}_{minlen}-{maxlen}aa.fasta")

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Collect sequences in a fasta file within a limited range.")
    parser.add_argument('infile', metavar='i', type=str, help='Input fasta file.')
    parser.add_argument('min_length', metavar='min', type=int, help='Minimum length allowed. Fasta entries greater than or equal to this length are kept.')
    parser.add_argument('max_length', metavar='max', type=int, help='Maximum length allowed. Fasta entries less than or equal to this length are kept.')
    parser.add_argument('outlabel', metavar='o', type=str, help='Name for the filtered fasta.')
    args = parser.parse_args()
    
    merge(args.infile, args.min_length, args.max_length, args.outlabel)