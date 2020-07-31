#!python3
import helper
import argparse
import os

def merge(fasta, mapping, sep, id_col, value_col, outfile):
    seqs = helper.ReadFasta( fasta )
    map = helper.ReadUniqueMapping( mapping, sep, id_col, value_col )
    
    out = {}
    unmapped = 0
    for header, seq in seqs.items():
        if header in map:
            out[map[header]] = seq
        else:
            out[header] = seq
            unmapped+=1
    print(f'{unmapped} sequences not renamed')
    helper.WriteFasta(out, outfile)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Rename the entries in a fasta file according to a mapping file.")
    parser.add_argument('fasta', metavar='f', type=str, help = 'Fasta file.')
    parser.add_argument('mapping', metavar='m', type=str, help = 'Mapping file, with 2 or more columns of data separated by a special character.')
    parser.add_argument('-id_col', metavar='-i', type=int, default=0, help = 'The position number of the column in the mapping file to use as the input id, 0 by default. Zero-indexed.')
    parser.add_argument('-value_col', metavar='-n', type=int, default=1, help = 'The position number of the column in the mapping file to use as the new id, 1 by default. Zero-indexed.')
    parser.add_argument('-sep', metavar='-s', type=str, default='\t', help = 'The character used to separate columns. TAB by default.')
    parser.add_argument('outfile', metavar='o', type=str, help = 'Name of extracted fasta file.')
    args = parser.parse_args()
    
    merge(args.fasta, args.mapping, args.sep, args.id_col, args.value_col, args.outfile)

