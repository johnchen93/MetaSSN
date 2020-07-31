#!python3
import helper
import argparse
import os

def extractRow(line, sep, col):
    row = line.split(sep)
    values = []
    for i in range(len(row)):
        v = row[i].strip()
        if i == col:
            key = v
        else:
            values.append(v)
    
    return key, values
    
def merge(t1, t2, sep1, sep2, id_col1, id_col2, h1, h2, outfile):
    
    tb1 = {}
    with open(t1,'r') as f:
        if h1:
            key_col1, hd1 = extractRow(next(f),sep1,id_col1)
        for line in f:
            if line.strip()=='':
                continue
            k, v = extractRow(line,sep1,id_col1)
            tb1[k] = v
            
    if not h1 and h2:
        hd1 = [ f"col:{x}" for x in range(len(v)) ] # use length of last column as headers
    
    with open(t2,'r') as f:
        if h2:
            key_col2, hd2 = extractRow(next(f),sep2,id_col2)
        for line in f:
            if line.strip()=='':
                continue
            k, v = extractRow(line,sep2,id_col2)
            if k in tb1:
                tb1[k] += v # extend the list
                
    if not h2 and h1:
        hd2 = [ f"col:{x}" for x in range(len(v)-len(hd1)) ]
        
    if not h1 and h2: # use the column 2 key header for the table
        key_col1 = key_col2
        
    if not h1 and not h2:
        hd1 = [ f"col:{x}" for x in range(len(tb1[list(tb1.keys())[0]])) ]
        hd2 = []
        key_col1 = "key"
        
    with open(outfile, 'w') as fo:
        # decide headers
        fo.write(f"{key_col1}{sep1}{sep1.join(hd1+hd2)}\n")
        for k, v in tb1.items():
            fo.write(f"{k}{sep1}{sep1.join(v)}\n")
   

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Takes two tables and merge them based on a key column.")
    parser.add_argument('table1', type=str, help='Input table 1. This is the MAIN table, only items that are found in this table will be returned in the final results.')
    parser.add_argument('table2', type=str, help='Input table 2. Entries that match the key column of table 1 will be appended to table 1.')
    parser.add_argument('outlabel', type=str, help='Output file for the merged table.')
    
    parser.add_argument('-id_col1', '-i1', metavar='NUM', type=int, default=0, help = 'The position number of the column to use as a key for table 1, 0 by default. Zero-indexed.')
    parser.add_argument('-id_col2', '-i2', metavar='NUM', type=int, default=0, help = 'The position number of the column to use as a key for table 2, 0 by default. Zero-indexed.')
    parser.add_argument('-sep1', '-s1', metavar='s', type=str, default='\t', help = 'The character used to separate columns in table 1. This will also be the separator format of the merged output table. TAB by default.')
    parser.add_argument('-sep2', '-s2', metavar='s', type=str, default='\t', help = 'The character used to separate columns in table 2. TAB by default.')
    parser.add_argument('-h1', action='store_true', help = 'Flag. Indicates that table 1 has a header.')
    parser.add_argument('-h2', action='store_true', help = 'Flag. Indicates that table 2 has a header.')
    args = parser.parse_args()
    
    merge(args.table1, args.table2, args.sep1, args.sep2, args.id_col1, args.id_col2, args.h1, args.h2, args.outlabel)