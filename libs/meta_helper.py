import os
import errno
import sys
from math import log10, floor

def readMembership(file):
    aslist = {} # key is metanode index, value is the list of all members
    asdict = {} # table format for look up when the cluster definition is a table, a dict with the member ids as keys and nodes as values
    with open(file, 'r') as f:
        next(f) # skip the header
        for line in f:
            row = line.split('\t')
            node = row[0].strip()
            seq = row[1].strip()
            if aslist.get(node) is None:
                aslist[node] = [seq]
            else:
                aslist[node].append(seq)
            asdict[seq] = node
    return aslist, asdict

def gatherFilter(filter_files):
    debugOut('Gathering sequence ID filters for metanode analysis.', 'start block')
    
    if len(filter_files) > 0:
        filter = []
        for file in filter_files:
            with open(f"{filter_path}{file}",'r') as f:
                debugOut(f'Adding members in file \'{file}\' to the filter.')
                for line in f:
                    id = line.strip()
                    if id != '':
                        filter.append(id)
    else:
        debugOut('No filters given.')
        filter = None    
    debugOut('Filter collection finished.','end block')
    
    return filter
    
def debugOut(msg, type='point'):
    if type=='start block':
        print('\n ---')
        print(f" + {msg}")
    elif type == 'point':
        print(f" - {msg}")
    elif type == 'subpoint':
        print(f"   - {msg}")
    elif type == 'end block':
        print(f" + {msg}")
        print(" ---")
    
def make_sure_path_exists(path):
    # recursively creates a series of directories if it does not already exist
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def auto_round(summ, sig=2): # round a list
    rounded = []
    for x in summ:
        if log10(abs(x)) >= sig:
            rounded.append(round(x))
        else:
            rounded.append(round_sig(x))
    return rounded
    