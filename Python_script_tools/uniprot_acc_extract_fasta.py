#!python3
import helper
import argparse
import os

def convert(infile, sep, id_col, conv_only, outfile):

    with open(infile, 'r') as f:
        with open(outfile, 'w') as fo:
            for line in f:
                row = line.split(sep)
                header = row[id_col].strip()
                id = header.split('|')[1]
                if conv_only:
                    fo.write(f"{id}\n")
                else:
                    fo.write(f"{line.strip()}\t{id}\n")
   

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Takes a file with a list of UniProt headers (can be a table, where the header is one of the columns), and extracts the UniProt accession.")
    parser.add_argument('infile', type=str, help='Input file with UniProt headers on each line.')
    parser.add_argument('outlabel', type=str, help='Output file for the headers.')
    
    parser.add_argument('-id_col', '-i', metavar='NUM', type=int, default=0, help = 'The position number of the column in the mapping file that contains the input identifiers, 0 by default. Zero-indexed.')
    parser.add_argument('-sep', '-s', metavar='s', type=str, default='\t', help = 'The character used to separate columns if the file is a table. TAB by default.')
    parser.add_argument('-converted_only', '-C', action='store_true', help='Flag. If set, the output will only contain the extracted accession.')
    args = parser.parse_args()
    
    convert(args.infile, args.sep ,args.id_col, args.converted_only, args.outlabel)