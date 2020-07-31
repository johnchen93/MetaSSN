#!python3
import helper
import argparse
import os

def convert(infile, mapping, sep, id_col, val_col, conv_only, outfile):

    map = {}
    with open(mapping, 'r') as f:
        for line in f:
            row = line.split(sep)
            map[row[id_col].strip()] = row[val_col].strip()
    
    with open(infile, 'r') as f:
        with open(outfile, 'w') as fo:
            for line in f:
                id = line.strip()
                if id in map:
                    if conv_only:
                        fo.write(f"{map[id]}\n")
                    else:
                        fo.write(f"{id}\t{map[id]}\n")
                else:
                    print(f"\'{id}\' was not found.")
   

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Takes a file with a list of identifiers (one per line), and extracts the equivalent identifier based on a mapping file. The mapping file is simply a list where each row contains both identifiers in different columns. The default expected separator between columns is TAB, but can be configured to be a different character. The default output is a file with the old and new headers side by side in each line.")
    parser.add_argument('infile', type=str, help='Input file with list of IDs.')
    parser.add_argument('mapping', metavar='m', type=str, help = 'Mapping file, with 2 or more columns of data separated by a special character.')
    parser.add_argument('outlabel', type=str, help='Output file for the headers.')
    
    parser.add_argument('-id_col', '-i', metavar='NUM', type=int, default=0, help = 'The position number of the column in the mapping file that contains the input identifiers, 0 by default. Zero-indexed.')
    parser.add_argument('-value_col', '-v', metavar='NUM', type=int, default=1, help = 'The position number of the column in the mapping file that contains the new identifiers, 1 by default. Zero-indexed.')
    parser.add_argument('-sep', '-s', metavar='s', type=str, default='\t', help = 'The character used to separate columns. TAB by default.')
    parser.add_argument('-converted_only', '-C', action='store_true', help='Flag. If set, the output will only contain the converted header.')
    args = parser.parse_args()
    
    convert(args.infile, args.mapping, args.sep ,args.id_col, args.value_col, args.converted_only, args.outlabel)