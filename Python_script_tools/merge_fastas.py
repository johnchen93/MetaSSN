#!python3
import helper
import argparse
import os

def merge(fastas, outfile):
    out = {}
    for f in [ x for x in fastas]:
        out.update(helper.ReadFasta( f ))
    helper.WriteFasta(out, outfile)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Combine all fasta files in a directory")
    parser.add_argument('outfile', metavar='o', type=str, help='Name for the merged fasta.')
    parser.add_argument('fastas', metavar='f', type=str, nargs=argparse.REMAINDER, help='List of fasta files, each separated by a space.')
    args = parser.parse_args()
    
    merge(args.fastas, args.outfile)