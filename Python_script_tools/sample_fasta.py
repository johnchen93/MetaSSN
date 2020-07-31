#!python3
import helper
import argparse
import os
import random

def sample(file, n, outfile, seed):
    seqs = helper.ReadFasta(file)
    if seed is not None:
        random.seed(seed)
    take = random.sample(seqs.keys(), n)
    
    out = {}
    for id in take:
        out[id] = seqs[id]
    helper.WriteFasta(out, outfile)
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Randomly sample sequences in a fasta file, sampling without replacement.")
    parser.add_argument('infile', metavar='i', type=str, help='Input fasta file.')
    parser.add_argument('sample_size', metavar='n', type=int, help='Number of sequences to sample.')
    parser.add_argument('outlabel', metavar='o', type=str, help='Name for the output fasta.')
    parser.add_argument('-seed', metavar='-s', type=float, help='Seed for the random number generator.')
    args = parser.parse_args()
    
    sample(args.infile, args.sample_size, args.outlabel, args.seed)