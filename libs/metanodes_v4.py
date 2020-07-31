from libs.meta_helper import *
import os
import time
import math
import multiprocessing as mp
from itertools import islice

def main():
    cluster_threshold = 115
    min_bitscore = 50
    
    # light test case
    cols={'q':0,'s':1,'b':11} # q=query, s=subject, e=e-value, b=bitscore
    dir = '../input/blast/'
    files = ['b1_all_by_all.txt','b2_vs_b1_all_blast.txt','b2_vs_b1_all_as_subject.txt']
    meta( [dir+x for x in files], f'ssn_test_{min_bitscore}min_{cluster_threshold}clust', cols=cols, cluster_threshold=cluster_threshold, min_bitscore = min_bitscore)

def meta(files, outname = None, cluster_threshold=100, min_bitscore=50, cols={'q':0,'s':1,'b':2}, sep='\t', filter=None, to_file=True, outfile_names=None):
    '''
        Version 2 - Comparison of sequences to existing metanodes is now conducted by using dictionaries 
                    rather than set operations. Untested whether this is faster, but it functions the same as the original in terms of output.
        Version 3 - Discontinued tracking of e-value for nodes. Members are still tracked but are not 
                    written into the node table anymore. Edge tables no longer have the linker pairs and linker count, since those are inaccurate if the edges are culled in anyway, which they almost always are.
        Version 4 - Instead of loading and prefiltering all the BLAST results, stream each file and 
                    process the results as they come. Minor optimizations were also made by making the dictionary keys strings instead of tuples. Wasteful memory usage has been addressed by not recording hits with scores below the min bitscore as putative linkers. Memory consumpution is down by 50% in the worst case where all edges get collected for linker detection, and memory consumption is minimal when the number of putative linkers is small (e.g., when the cluster and min bitscores are close to each other). The results have been tested and are the exact same as V3 in terms of sequence membership in nodes as well as network connections. The overall run time is down by 50% from V3 (~11min to ~6min for an equivalent set of cut-offs). There was also a failed attempt to try multiprocessing, but it ended up being slower.
        
        Inputs:
            files - List of strings. Path to BLAST result files to use for metanode analysis
            outname - String. Name of analysis results. The output files will have this as the main identifier with suffixes attached.
            cluster_threshold - Number. The threshold at which different sequences in the BLAST results will be grouped into the same metanode. Expressed in bit_score.
            min_bitscore - Number. The lowest threshold to permit connecting edges between metanodes. Expressed in bit_score.
            cols - Dictionary with column indices as values. A mapping for which columns in the BLAST results file contains desired information. The contents should include: 'q' - column for query ID, 's' - column for subject ID, 'e' - column for E-value, 'b' - column for bit_score
            sep - String. Character used to separate columns in the BLAST result file. Defaults are not accurate, simply placeholders.
            filter - List. If given, only sequence IDs in this list will be considered for the network analysis.
        
        Outputs:
            3 files are created upon running the program.
            <outname>_meta-node_members.txt - A file that records the metanode membership of each sequence in the BLAST results input.
            <outname>_meta-node_summary.txt - A file that records information about each metanode, including the number and identity of member sequences. Used as the nodes table for a network.
            <outname>_meta-network.txt - A describing connection between metanodes. Used as the edge table for a network.
    '''
    debugOut(f"Started metanode analysis : {time.asctime()}")
    debugOut(f"Starting metanode analysis for {outname} at {min_bitscore} min edge bitscore and {cluster_threshold} grouping bitscore.",'start block')
    if outname is None and outfile_names is None:
        debugOut("Analysis has no name. Exiting.",'end block')
        return
    # prepare sequence filter
    to_take = {}
    if filter is not None:
        debugOut('Sequence filter supplied. Preparing filter.')
        for x in filter:
            to_take[x] = True
            
    
    # first pass - read data and generate metanodes
    debugOut('Loading BLAST results.')
    debugOut('Grouping members into metanodes')
    
    metanodes = {} # each sequence ID
    node_index = 0
    putative_linker = {}
    line_count=0
    for file in files:
        f = open(file,'r')
        
        for line in f:
            if line.strip()=='':
                continue
            line_count += 1    
            # parse hit results
            fields = line.strip().split(sep)
            bitscore = float(fields[cols['b']])
            query = fields[cols['q']]
            subject = fields[cols['s']]
            
            if filter is not None: # if filter is given, only take blast pairs where both sequences are within the filter
                if (query not in to_take) or (subject not in to_take):
                    continue
            
            # build metanodes
            s1 = min(query,subject)
            s2 = max(query,subject)
            label = f"{s1}~~~{s2}"
            
            n1, n2 = metanodes.get(s1), metanodes.get(s2) # get metanode index
        
            if bitscore<cluster_threshold: # save non clustering pairs for later
                if bitscore>=min_bitscore:
                    putative_linker[label] = bitscore
                    
                if n1 is None: # when two sequences are below the threshold, each creates a new metanode if not attached to an existing metanode
                    metanodes[s1] = node_index
                    node_index+=1
                if n2 is None:
                    metanodes[s2] = node_index
                    node_index+=1    
                continue
                
            # score above limit metanodes should be connected    
            # if both are new, increase node count and set in metanodes
            if (n1 is None) and (n2 is None):
                metanodes[s1] = node_index
                metanodes[s2] = node_index
                node_index += 1
            # if one is new, set the new sequence to be the same metanode as the other existing one
            elif (n1 is None) != (n2 is None): # excludes the case where both are new (addressed above) or both are existing (addressed below)
                if n1 is None: # n1 is the new one, set to same metanode as n2
                    metanodes[s1] = n2
                elif n2 is None: # n2 is the new one, set to same metanode as n1
                    metanodes[s2] = n1
            # if both are existing - decide next action
            elif (n1 is not None) and (n2 is not None):
                # if both are within the same metanode - do nothing
                if n1 == n2:
                    pass
                # if both are in different metanodes - merge the metanodes, keeping the lower metanode index
                elif n1 != n2:
                    tar = max(n1,n2) # node index to replace
                    new = min(n1,n2) # new node index
                    for k, v in metanodes.items():
                        if v==tar:
                            metanodes[k] = new
            
        f.close()
        sys.stdout.write(f"\r - {line_count} entries processed.")
        sys.stdout.flush()
        
    print('\n')
    
    # second pass - renumber metanodes to remove gaps in numbering
    order = {}
    node_IDs = sorted(list(set(metanodes.values())))
    for i in range( len(node_IDs) ):
        order[node_IDs[i]]=i
    # re-assign the new node indices
    for k, v in metanodes.items():
        metanodes[k] = order[v]
    
    # third pass - find lower bitscore edges
    debugOut('Generating edges between metanodes.')
    edges = {}
    for label, bitscore in putative_linker.items():
        if bitscore<min_bitscore:
            continue
        label_parts = label.split('~~~')
        s1, s2 = label_parts[0], label_parts[1]
        n1, n2 = metanodes.get(s1), metanodes.get(s2) # get metanode index
        
        if n1 != n2:
            con_id = f"{min(n1,n2)}<|>{max(n1,n2)}"
            old_score = edges.get(con_id)
            if (old_score is None) or old_score < bitscore:
                edges[con_id] = bitscore

    # collect node membership
    membership = {}
    for seq, node in metanodes.items():
        if not membership.get(node):
            membership[node] = [seq]
        else:
            membership[node].append(seq)
    
    debugOut(f"Analysis generated {len(membership.keys())} metanodes connected by {len(edges.keys())} edges.")
    
    # directly return output dicts, mostly for internal use
    if not to_file:
        return {'membership':membership,
                'nodes':metanodes,
                'edges':edges}
                
    # organize outfile names
    if outfile_names is not None:
        outnames = outfile_names
    else:
        outnames = {'membership':outname+f'_meta-node_members.txt',
                    'nodes':outname+f'_meta-node_summary.txt',
                    'edges':outname+f'_meta-network.txt'}            
    # write output
    debugOut(' - Writing metanode analysis output to file.')
    with open(outnames['membership'],'w') as f:
        with open(outnames['nodes'],'w') as s:
            
            f.write('\t'.join(['node','member'])+'\n')
            s.write('\t'.join(['node','member_count'])+'\n')
            for node, members in membership.items(): # renumber nodes to be consecutive
                for x in members:
                    f.write(f'{node}\t{x}\n')
                s.write(f'{node}\t{len(members)}\n')
            
    headers = ['node1','node2','bitscore']
    with open(outnames['edges'],'w') as f:
        f.write('\t'.join(headers+['id'])+'\n')
        for con_id, bit_score in edges.items():
            edge_list = con_id.split('<|>')
            n1, n2 = edge_list[0], edge_list[1]
            f.write(f'{n1}\t{n2}\t{bit_score}\n')
        # make self edges for each metanode, so they will show up in the network regardless of connectivity 
        for node_id in order.values():
            f.write(f'{node_id}\n')
    debugOut("Metanode analysis complete.", 'end block')
    debugOut(f"Finished metanode analysis : {time.asctime()}")
    return outnames
    
if __name__ == '__main__':
    main()
                        