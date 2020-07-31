#!python3
import helper
import argparse
import os

def doTheThing(infile, outfile):
    seqs = helper.ReadFasta( infile )
    out = {}
    for header, seq in seqs.items():
        out[header] = seq.replace('-','')
    helper.WriteFasta(out, outfile)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Extract the sequence from an aligned fasta file.")
    
    parser.add_argument('aligned_fasta', metavar='f', type=str, help='Aligned fasta file used as input.')
    parser.add_argument('outfile', metavar='o', type=str, help='Name for the merged fasta.')
    args = parser.parse_args()
    
    doTheThing(args.aligned_fasta, args.outfile)