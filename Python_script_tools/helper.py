import errno
import os
import string
import gzip

# single letter list of amino acids, sorted by type
aa_list = ['H', 'K', 'R',                # (+)
           'D', 'E',                     # (-)
           'C', 'M', 'N', 'Q', 'S', 'T', # Polar-neutral
           'A', 'G', 'I', 'L', 'P', 'V', # Non-polar
           'F', 'W', 'Y',                # Aromatic
           '*']

# codon table
CODON_TABLE = {
        'TTT':'F', 'TCT':'S', 'TAT':'Y', 'TGT':'C',
        'TTC':'F', 'TCC':'S', 'TAC':'Y', 'TGC':'C',
        'TTA':'L', 'TCA':'S', 'TAA':'*', 'TGA':'*',
        'TTG':'L', 'TCG':'S', 'TAG':'*', 'TGG':'W',
        'CTT':'L', 'CCT':'P', 'CAT':'H', 'CGT':'R',
        'CTC':'L', 'CCC':'P', 'CAC':'H', 'CGC':'R',
        'CTA':'L', 'CCA':'P', 'CAA':'Q', 'CGA':'R',
        'CTG':'L', 'CCG':'P', 'CAG':'Q', 'CGG':'R',
        'ATT':'I', 'ACT':'T', 'AAT':'N', 'AGT':'S',
        'ATC':'I', 'ACC':'T', 'AAC':'N', 'AGC':'S',
        'ATA':'I', 'ACA':'T', 'AAA':'K', 'AGA':'R',
        'ATG':'M', 'ACG':'T', 'AAG':'K', 'AGG':'R',
        'GTT':'V', 'GCT':'A', 'GAT':'D', 'GGT':'G',
        'GTC':'V', 'GCC':'A', 'GAC':'D', 'GGC':'G',
        'GTA':'V', 'GCA':'A', 'GAA':'E', 'GGA':'G',
        'GTG':'V', 'GCG':'A', 'GAG':'E', 'GGG':'G'
    }

#: Conversions between single- and three-letter amino acid codes
AA_CODES = {
        'Ala' : 'A', 'A' : 'Ala',
        'Arg' : 'R', 'R' : 'Arg',
        'Asn' : 'N', 'N' : 'Asn',
        'Asp' : 'D', 'D' : 'Asp',
        'Cys' : 'C', 'C' : 'Cys',
        'Glu' : 'E', 'E' : 'Glu',
        'Gln' : 'Q', 'Q' : 'Gln',
        'Gly' : 'G', 'G' : 'Gly',
        'His' : 'H', 'H' : 'His',
        'Ile' : 'I', 'I' : 'Ile',
        'Leu' : 'L', 'L' : 'Leu',
        'Lys' : 'K', 'K' : 'Lys',
        'Met' : 'M', 'M' : 'Met',
        'Phe' : 'F', 'F' : 'Phe',
        'Pro' : 'P', 'P' : 'Pro',
        'Ser' : 'S', 'S' : 'Ser',
        'Thr' : 'T', 'T' : 'Thr',
        'Trp' : 'W', 'W' : 'Trp',
        'Tyr' : 'Y', 'Y' : 'Tyr',
        'Val' : 'V', 'V' : 'Val',
        'Ter' : '*', '*' : 'Ter',
        '???' : '?', '?' : '???'
}

# translation table for reverse complementing from Enrich2
dna_trans = str.maketrans("actgACTG", "tgacTGAC")

def RevComp(seq):
        """
        Reverse-complement the sequence
        """
        return seq.translate(dna_trans)[::-1]
        
def MyOpen(infile, mode="r"):
    if infile.endswith(".gz"):
        return gzip.open(infile, mode=mode)
    else:
        return open(infile, mode=mode)
        
# general fasta parser that takes multiline fastas and returns the sequence as a value in a dictionary
# where the key is the header
def ReadFasta(infile):
    sequences = {}
    with open(infile,'r') as f_in:
        currheader = ""
        for line in f_in:
            if line.strip()=="": # skip empty lines
                continue
            if line.startswith(">"):
                currheader = line[1:].strip()
                sequences[currheader] = []
            else:
                sequences[currheader].append(line.rstrip())

    for k,v in sequences.items():
        # make multiline sequences a single entry
        sequences[k] = "".join(v)

    return sequences

def WriteFasta(dict, outfile):
    with MyOpen(outfile, 'w') as f:
        for header, seq in dict.items():
            f.write(f">{header}\n{seq}\n")

def ReadLines(infile):
    out = []
    with open(infile,'r') as f_in:
        for line in f_in:
            value = line.strip()
            if value=="":
                continue
            out.append(value)
    return out   

def ReadUniqueMapping(infile, sep='\t', id_col = 0, value_col = 1):
    out = {}
    with open(infile, 'r') as f_in:
        for line in f_in:
            value = line.strip()
            if value=="":
                contiue
            row = value.split(sep)
            out[row[id_col]] = row[value_col]
    return out
    
def rStr(num,x):
    return str(round(num,x))

def HammingDistance(s1, s2):
    """Calculate the Hamming distance between two bit strings
    returns just the hamming distance"""
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def Differences(s1, s2):
    """Calculate the Hamming distance between two bit strings
    returns the full list of booleans, where true indicates a mismatch"""
    assert len(s1) == len(s2) # assume, since assert and try except don't work with jit
    return [c1 != c2 for c1, c2 in zip(s1, s2)]

def CodonDifferences(s1, s2):
    """Calculate codon differences

    Input:
    s1 - a string of DNA, divisible by 3, in frame with intended reading frame
    s2 - similar to s1, must be same length
    """
    assert len(s1) == len(s2)
    return [s1[i:i+3] != s2[i:i+3] for i in range(0, len(s1),3)]


def Translate(dna):
    return "".join(CODON_TABLE[dna[i:i+3]] for i in range(0, len(dna),3))

def GetSubdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def GetFilesInDir(mypath):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        f.extend(filenames)
        break
    return filenames

def MakeSurePathExists(path):
    # recursively creates a series of directories if it does not already exist
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
            