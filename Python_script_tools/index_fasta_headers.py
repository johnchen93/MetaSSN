#!python3
import helper
import argparse
import os

def merge(infile, outfile):
    seq = helper.ReadFasta( infile )
    with open(outfile+'_map','w') as f:
        out = {}
        i = 0
        for header, sequence in seq.items():
            out[i] = sequence
            f.write(f"{i}\t{header}\n")
            i+=1
            
    helper.WriteFasta(out, f"{outfile}.fasta")

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Takes a fasta file and converts the sequence headers to numberical indices.")
    parser.add_argument('infile', metavar='i', type=str, help='Input fasta file.')
    parser.add_argument('outlabel', metavar='o', type=str, help='Label for the converted fasta file and the mapping file, should exclude filetype suffixes.')
    args = parser.parse_args()
    
    merge(args.infile, args.outlabel)