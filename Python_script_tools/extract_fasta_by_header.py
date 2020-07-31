#!python3
import helper
import argparse
import os

def merge(headers, fasta, outfile):
    seq = helper.ReadFasta( fasta )
    tar = helper.ReadLines( headers )
    
    out = {}
    for header in tar:
        if header in seq:
            out[header] = seq[header]
    helper.WriteFasta(out, outfile)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Extract entries from a fasta file by a given list of headers.")
    parser.add_argument('headers', metavar='h', type=str, help = 'File of desired headers from the fasta with one header per line.')
    parser.add_argument('fasta', metavar='f', type=str, help = 'Fasta file.')
    parser.add_argument('outfile', metavar='o', type=str, help = 'Name of extracted fasta file.')
    args = parser.parse_args()
    
    merge(args.headers, args.fasta ,args.outfile)

