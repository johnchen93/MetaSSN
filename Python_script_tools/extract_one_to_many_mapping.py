#!python3
import helper
import argparse
import os

def convert(infile, mapping, sep, id_col, val_col, conv_only, outfile):
    
    ids = {}
    with open(infile, 'r') as f:
        for line in f:
            id = line.strip()
            ids[id] = True
        
    with open(mapping, 'r') as f:
        with open(outfile, 'w') as fo:
            for line in f:
                row = line.split(sep)
                cur_id = row[id_col].strip()
                if cur_id in ids:
                    val = row[val_col].strip()
                    if conv_only:
                        fo.write(f"{val}\n")
                    else:
                        fo.write(f"{cur_id}\t{val}\n")
   

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Takes a file with a list of identifiers (one per line), and extracts the equivalent identifiers based on a mapping file. The mapping file is simply a list where each row contains both identifiers in different columns. The default expected separator between columns is TAB, but can be configured to be a different character. The default output is a file with the old and new headers side by side in each line.")
    parser.add_argument('infile', type=str, help='Input file with list of IDs.')
    parser.add_argument('mapping', metavar='m', type=str, help = 'Mapping file, with 2 or more columns of data separated by a special character.')
    parser.add_argument('outlabel', type=str, help='Output file for the extracted IDs. By default, the ID used to extract will be listed in the first column and the extracted IDs will be in the second column. Set the -converted_only flag to only receive a single column with the extracted IDs.')
    
    parser.add_argument('-id_col', '-i', metavar='NUM', type=int, default=0, help = 'The position number of the column in the mapping file that contains the input identifiers, 0 by default. Zero-indexed.')
    parser.add_argument('-value_col', '-v', metavar='NUM', type=int, default=1, help = 'The position number of the column in the mapping file that contains the new identifiers, 1 by default. Zero-indexed.')
    parser.add_argument('-sep', '-s', metavar='s', type=str, default='\t', help = 'The character used to separate columns. TAB by default.')
    parser.add_argument('-converted_only', '-C', action='store_true', help='Flag. If set, the output will only contain the converted header.')
    args = parser.parse_args()
    
    convert(args.infile, args.mapping, args.sep ,args.id_col, args.value_col, args.converted_only, args.outlabel)