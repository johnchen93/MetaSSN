#!python3
import helper
import argparse
import os

def extract_header(infile, outfile):
    seq = helper.ReadFasta( infile )
    with open(outfile,'w') as f:
        for header, sequence in seq.items():
            f.write(f"{header}\n")
            

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Takes a fasta file and extracts just the headers, ignoring the \'>\' at the start.")
    parser.add_argument('infile', metavar='i', type=str, help='Input fasta file.')
    parser.add_argument('outlabel', metavar='o', type=str, help='Output file for the headers.')
    args = parser.parse_args()
    
    extract_header(args.infile, args.outlabel)