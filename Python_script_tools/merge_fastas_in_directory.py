#!python3
import helper
import argparse
import os

def merge(dir, outfile):
    out = {}
    for f in [ x for x in helper.GetFilesInDir(dir) if x.endswith('.fasta')]:
        out.update(helper.ReadFasta( os.path.join(dir,f) ))
    helper.WriteFasta(out, outfile)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Combine all fasta files in a directory")
    parser.add_argument('directory', metavar='d', type=str, help='Folder where the fasta files are.')
    parser.add_argument('outfile', metavar='o', type=str, help='Name for the merged fasta.')
    args = parser.parse_args()
    
    merge(args.directory, args.outfile)