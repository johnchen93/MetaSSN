# from libs.metanodes_v3 import meta, remeta
from libs.metanodes_v4 import meta
from libs.decluster import declusterDict
from libs.map_member_names import map
from libs.meta_helper import *
import os
import argparse
import importlib
     

#                   ***************************************
#                   ********     Program Set-up    ********
#                   ***************************************
        
# check command line arguments, overrides manual settings if applicable
# two possible command modes
# meta_network
parser = argparse.ArgumentParser(description="Generate and annotate an SSN based on settings in the config.py.")
parser.add_argument('edge_bitscore', metavar='edge_bitscore', type=int, help='An integer. Bitscore threshold for the edges between nodes. BLAST results with a bitscore equal or above this threshold and will be considered for an edge connection between metanodes, while those below the threshold are excluded from the network.')
parser.add_argument('cluster_bitscore', metavar='cluster_bitscore', type=int, help='An integer. Bitscore threshold for clustering sequences into the same metanode. BLAST results with a bitscore equal to or above this thresholf will be merged into the same metanode.')
parser.add_argument('-sweep_interval', '-si', metavar='NUM', type=int, help='An integer. If this option is specified, the program will construct a series of SSNs starting from the edge_bitscore and the cluster_bitscore with a fixed range between the edge bitscore and cluster bitscore. For example, with an edge bitscore of 100 and a cluster bitscore of 200, setting sweep_envelope to 50 will generate the networks at 50-100, 100-150 and 150-200 bitscores.')
parser.add_argument('-cluster_interval', '-ci', metavar='NUM', type=int, help='An integer. If this option is specified, the program will construct a series of SSNs starting from the edge_bitscore up to the cluster_bitscore, at steps of increasing cluster_bitscore according to cluster_interval. For example, with an edge bitscore of 100 and a cluster bitscore of 200, setting cluster_interval to 50 will generate the networks at 100-150 and 100-200.')

parser.add_argument('-config_file', '-cf', metavar='STR', type=str, help='Provide the name of the config file that you wish to use, including the .py extension. The config file needs to be in the same directory as this script.')

parser.add_argument('-label', '-l', metavar='STR', type=str, help='Label to use for this set of SSNs, overrides the label given in the config file.')
parser.add_argument('-output_dir', '-o', metavar='STR', type=str, help='Directory to store output for this set of SSNs, overrides the path given in the config file.')

parser.add_argument('-rebuild_networks', '-R', action='store_true', help='Force MetaSSN to reconstruct networks even if an older one with the same thresholf already exists')
parser.add_argument('-skip_declustering', '-SD', action='store_true', help='MetaSSN will not use CD-hit information to decluster member sequences of each node into full sequence sets.')
parser.add_argument('-redo_declustering', '-RD', action='store_true', help='MetaSSN will redo declustering member sequences of each node into full sequence sets even if an older declustering was found.')
parser.add_argument('-skip_annotation', '-SA', action='store_true', help='MetaSSN will not try to annotate the metaNodes.')
args = parser.parse_args()

# load config file
if args.config_file is not None:
    config_file_exists = os.path.isfile(args.config_file) and args.config_file.endswith('.py')
    if config_file_exists:
        config = importlib.import_module(args.config_file[:-3])
    else:
        print('Error : Failed to load the config file. Try checking the spelling of the config file, making sure it is a python file (\'.py\' extension). Also make sure the config file is in the same directory as this script.')
        quit()
else:
    config_file_exists = os.path.isfile('config.py')
    if config_file_exists:
        import config
    else:
        print('Error : Attempt to load default config file (config.py) failed. If you have set your run configurations in the default file, make sure it is in the same directory as this script. To use another config file, provide a separate config file using the \'-config_file\' option.')
        quit()

# load configurations
blast_results_path = config.blast_results_path
blast_results_files = config.blast_results_files
query_col = config.query_col
subject_col = config.subject_col
bitscore_col = config.bitscore_col
filter_path = config.filter_path
filter_files = config.filter_files
output_label = config.output_label
output_dir = config.output_dir
mapping_path = config.mapping_path
member_name_mapping = config.member_name_mapping
cluster_info_path = config.cluster_info_path
cluster_file_info = config.cluster_file_info
cdhit_heirarchy = config.cdhit_heirarchy
annot_path = config.annot_path
membership_count_annot = config.membership_count_annot
membership_freq_annot = config.membership_freq_annot
membership_label = config.membership_label
membership_dist_annot = config.membership_dist_annot
membership_lower_node = config.membership_lower_node

# Read command line input
# determine clustering thresholds
if args.sweep_interval is not None:
    bitscore_gap = args.sweep_interval
    metanode_bitscore_range = range(args.edge_bitscore, args.cluster_bitscore+bitscore_gap, bitscore_gap)
    fixed_min_bitscore = None
elif args.cluster_interval is not None:
    bitscore_gap = None
    metanode_bitscore_range = range(args.edge_bitscore+args.cluster_interval, args.cluster_bitscore+args.cluster_interval, args.cluster_interval)
    fixed_min_bitscore = args.edge_bitscore
else:
    bitscore_gap = None
    metanode_bitscore_range = [args.cluster_bitscore]
    fixed_min_bitscore = args.edge_bitscore

# determine other settings
# lay out some default behaviors
use_old_metanodes = True # use network old if found
analyze_clustering = True # try to analyze clustering if a set of cd-hit files is provided in the config
use_old_clustering = True # if an old cluster file with the same settings alread exists, re-use it
annot_metanodes = True # apply annotations

if args.label is not None:
    output_label = args.label
if args.output_dir is not None:
    output_dir = args.output_dir
    
if args.rebuild_networks:
    use_old_metanodes = False
if args.skip_declustering:
    analyze_clustering = False
if args.redo_declustering:
    use_old_clustering = False
if args.skip_annotation:
    annot_metanodes = False

# misc settings, no need for modification
annotation_data_sets = [membership_count_annot, membership_freq_annot, membership_label, membership_dist_annot, membership_lower_node]
default_annot_values = {'count':0, 'freq':'','label':'','dist':'','lower node':''}

# -------------------------------------------------------------------
    
#                   ***************************************
#                   ********     Analysis Code     ********
#                   ***************************************

# file naming structure
suffixes = {'membership':'membership','nodes':'node_summary','edges':'network','all_seq':'node_all_seqs'}
name_pattern = "{name}_{min}-{max}clust_{suffix}.txt"

def generateNames(min, max):
    out = {}
    for k, v in suffixes.items():
        out[k] = os.path.join( output_dir, name_pattern.format(name=output_label, min=min, max=max, suffix=v) )
    return out 

def findOldAnalysis(files):
    for f in files:
        if not os.path.exists(f):
            return False
    return True
    
def createNetwork():
    # ======== set up for metanode generation ========
    # make sure out path exists
    make_sure_path_exists(output_dir)
    # assign data columns in BLAST file
    cols={'q':query_col,'s':subject_col,'b':bitscore_col} # q=query, s=subject, e=e-value, b=bitscore
    # collect sequence filter
    filter = gatherFilter(filter_path, filter_files)
    filter_label = "" if filter is None else "filtered_"
    
    # gather annotation levels, only needs to be done once
    annotations = {}
    freq_limits = {}
    for x in annotation_data_sets: # check the required annotations are present, at least in the header
        for v in x:
            stat = f"{v['level']}:{v['label']}"
            if x is membership_count_annot: # required if the annotations are skipped on the first pass
                annotations[stat] = "count"
            elif x is membership_freq_annot:
                annotations[stat] = "freq"
                freq_limits[stat] = v['highest_entries']
            elif x is membership_label:
                annotations[stat] = "label"
            elif x is membership_dist_annot:
                annotations[stat] = "dist"
            elif x is membership_lower_node:
                annotations[stat] = "lower node"
                
    #checked the contents of 'annotations' is correct
    
    
    # organize the bitscore cut-offs for metanode analysis
    # bitscore_range = sorted(set(metanode_bitscore_range), reverse=True)
    bitscore_range = sorted(set(metanode_bitscore_range))
    outfiles = None
    # find BLAST results
    if blast_results_files is None:
        _, _, filenames = next(os.walk(blast_results_path))
        blast_input = filenames
    else:
        blast_input = blast_results_files
    blast_input = [blast_results_path+x for x in blast_input]
    # start analysis cycle
    for metanode_bitscore in bitscore_range:
        if fixed_min_bitscore is not None:
            analysis_min_bitscore = fixed_min_bitscore
        else:
            analysis_min_bitscore = metanode_bitscore - bitscore_gap
            
        debugOut(f'Conducting analysis cycle for metanode generation at {metanode_bitscore} bitscore, with minimum edge {analysis_min_bitscore} bitscore.','start block')
        expected_files = generateNames(analysis_min_bitscore, metanode_bitscore)
        old_files_found = findOldAnalysis([expected_files['membership'],expected_files['nodes'],expected_files['edges']])
        # metanode clustering    
        if not use_old_metanodes or (use_old_metanodes and not old_files_found):
            outfiles = meta( blast_input , outname=output_label, cols=cols, cluster_threshold=metanode_bitscore, min_bitscore=analysis_min_bitscore, sep='\t', filter = filter, outfile_names = expected_files )
        else:
            debugOut('Using old metanode definitions.','end block')
            outfiles = expected_files
        # remap node members, if given
        for map_file in member_name_mapping:
            map(outfiles['membership'], f"{mapping_path}{map_file}")
        
        # ======== decluster members if the option is selected =========
        # resolve cluster sequences by metanode
        
        seq_by_node, seq_by_node_table = None, None
        if analyze_clustering:
            debugOut('Cluster analysis selected.','start block')
            old_cluster_file = expected_files['all_seq'] if findOldAnalysis([expected_files['all_seq']]) else None
            print(old_cluster_file)
            if not use_old_clustering or (use_old_clustering and old_cluster_file is None):
                seq_by_node, seq_by_node_table = clusterAnalysis(outfiles['membership'])
                with open(expected_files['all_seq'],'w') as f:
                    f.write('\t'.join(['node','sequence'])+'\n') # write the header
                    for node, seqs in seq_by_node.items():
                        for seq in seqs:
                            f.write(f'{node}\t{seq}\n') # write all sequences to the file
            else:
                debugOut(f'Using previous clustering at {metanode_bitscore} clustering bitscore and {analysis_min_bitscore} min bitscore','end block')
                seq_by_node, seq_by_node_table = readMembership(old_cluster_file)
            
        # further annotations
        if annot_metanodes:
            debugOut('Processing additional annotations.','block start')
            reps_by_node,  reps_by_node_table = readMembership(outfiles['membership'])
            
            node_stats = {} # storage for all node level annotations
            for node, reps in reps_by_node.items():
                node_stats[node] = { 'member_count':len(reps),'seq_count':0 }
                
            if seq_by_node is not None: # skip if declustering was not conducted
                for node, seqs in seq_by_node.items():
                    node_stats[node]['seq_count'] = len(seqs) # get the number of sequences per node, as opposed to just the representatives
            else:
                debugOut('Annotations are restricted to the \'member\' level, as declustering was not conducted, or the previous declustering file was not found.')
                
            annotate(node_stats, reps_by_node_table, seq_by_node_table, annotations, freq_limits)
            debugOut('Updating metanode summary file with new annotations.')
            stat_order = node_stats[list(node_stats.keys())[0]].keys() # grab second level headers from an arbitrary node
            with open(outfiles['nodes'],'w') as f:
                header = 'node' + "\t" + '\t'.join(stat_order) + '\n'
                f.write(header)
                for node in node_stats.keys():
                    f.write(f"{node}\t"+'\t'.join([str(node_stats[node][stat]) for stat in stat_order]) + '\n')
                        
            debugOut('Annotations complete.','end block')
    
# ===============  Helper functions ================
def clusterAnalysis(members_file):
    debugOut('Attempting to decluster representative sequences.','start block')
    # collect node membership
    debugOut('Retrieving all metanode members.')
    reps_by_node, reps_by_node_table = readMembership(members_file)
    
    # go through each given cluster file
    debugOut(f'Searching for given cluster files in \'{cluster_info_path}\'.')
    seq_by_node = {}
    for file, info in cluster_file_info.items():
        # cdhit cluster file
        if info['format']=='cdhit':
            files_input = [file]
            if cdhit_heirarchy is not None and cdhit_heirarchy.get(file):
                files_input += cdhit_heirarchy[file] # extend the list
            # prepend the path
            files_input = [cluster_info_path+f for f in files_input]
            print(f' - Input: CD-hit cluster file(s) {", ".join(files_input)} detected.')
            print('   - Declustering metanode members.')
            # run cdhit declustering code for each metanode group
            out = declusterDict(files_input, look_for_dict=reps_by_node)
            for node, reps in out.items():
                if seq_by_node.get(node) is None:
                    seq_by_node[node] = reps
                else:
                    seq_by_node[node].extend(reps)
                
        # table format, such as uniref table
        elif info['format']=='table':
            print(f' - Input: cluster table file {file} detected.')
            print('   - Declustering metanode members:')
            delim = info['delim']
            ki = info['key_col']
            mi = info['member_col']
            mdelim = info['member_delim']
            with open(cluster_info_path+file, 'r') as f:
                next(f) # clear the header
                for line in f:
                    row = line.split(delim)
                    key = row[ki].strip()
                    # iterate through each metanode
                    if key in reps_by_node_table:
                        node = reps_by_node_table[key]
                        out = [ x.strip() for x in row[mi].split(mdelim) ]
                        if node not in seq_by_node:
                            seq_by_node[node] = out
                        else:
                            seq_by_node[node].extend(out)
    
    seq_by_node_table = {}
    for node, seqs in seq_by_node.items():
        for seq in seqs:
            seq_by_node_table[seq] = node 
            
    debugOut('Declustering complete','end block')
    # return seq_by_node, reps_by_node, seq_by_node_table, reps_by_node_table
    return seq_by_node, seq_by_node_table

def annotate(node_stats, reps_by_node_table, seq_by_node_table, annotations, freq_limits):
    
    debugOut('Compiling annotations.', 'start block')
    # count based annotation
    for annot_set in annotation_data_sets:
        for info in annot_set:
            if info['level'] == 'member':
                node_ref = reps_by_node_table
            elif info['level'] == 'sequence':
                if seq_by_node_table is None:
                    continue # skip to the next file
                node_ref = seq_by_node_table
            stat_header = f"{info['level']}:{info['label']}"
            annot_type = annotations[stat_header]
            delim, id_col, data_col = info.get('delim'), info.get('id_col'), info.get('data_col')
            parse_table = delim is not None and id_col is not None and data_col is not None
            
            
            files = info['files']
            if type(files) == type(""):
                files = [files]
            agg = {} # data collection container
            for node, _ in node_stats.items():
                node_stats[node][stat_header] = default_annot_values[annot_type] # initialize count for all nodes
                agg[node] = []
            for file in files:
                with open(f"{annot_path}{file}",'r') as f: # try to open the file
                    debugOut(f'Annotating by \'{annot_type}\' for members in file \'{file}\' for \'{info["label"]}\' label at the \'{info["level"]}\' level.')
                    
                    for curline in f:
                        line = curline.strip()
                        if line=="":
                            continue
                        if parse_table:
                            row = line.split(delim)
                            id = row[id_col].strip()
                            val = row[data_col].strip()
                        else: # counting
                            id = line.strip()
                            val = 1
                        if id in node_ref: # if all reps are unique, this should indicate one match
                            agg[node_ref[id]].append(val)
                    # summarize and/or format results
            if annot_type == 'count':
                for node, values in agg.items():
                    node_stats[node][stat_header] = sum(values)
            elif annot_type == 'freq':
                tally = {}
                for node, values in agg.items():
                    tally[node] = {}
                    for v in values: # count occurences of each unique value
                        if v not in tally[node]:
                            tally[node][v] = 1
                        else:
                            tally[node][v] += 1
                formatFreq(node_stats, stat_header, tally, freq_limits[stat_header])
            elif annot_type == 'label':
                for node, values in agg.items():
                    node_stats[node][stat_header] = ','.join(sorted(set(values)))
            elif annot_type == 'dist':
                for node, values in agg.items(): # calculate the 5 number summary
                    s = sorted( float(x) for x in values)
                    l = len(s)
                    if l > 5:
                        if l%2==0:
                            h = l//2-1 # e.g. 8/2-1 = 3, 4th index 
                            m = (s[h] + s[h+1]) / 2
                            lq = s[:h]
                            uq = s[h:]
                        else:
                            h = l//2 # 9//2 = 4, 5th index
                            m = s[h]
                            lq = s[:h]
                            uq = s[h+1:]
                        qlen = len(lq)
                        if qlen%2==0:
                            q1 = (lq[qlen//2-1] + lq[qlen//2]) / 2
                            q3 = (uq[qlen//2-1] + uq[qlen//2]) / 2
                        else:
                            q1 = lq[qlen//2]
                            q3 = uq[qlen//2]
                        summ = [s[0],q1,m,q3,s[-1]]
                        rounded = auto_round(summ)
                        out = f"{'-'.join( str(x) for x in rounded )}(n={l})"    
                    else:
                        out = ','.join( str(x) for x in auto_round(s) )
                    node_stats[node][stat_header] = out
            elif annot_type == 'lower node':
                for node, values in agg.items():
                    if len(values) > 0:
                        node_stats[node][stat_header] = values[0] # if correct, all values should be the same
                    
    debugOut('Annotations finished.', 'end block')

def formatFreq(node_stats, stat_header, freq, entry_limit): # freq dict to string
    for node, tally in freq.items():
        total = sum(tally.values())
        order = [ (k, v, v/total*100) for k, v in tally.items() ]
        order = sorted(order, reverse=True, key=lambda x: x[1]) # sort by the count (2nd value)
        cur_entry_limit = entry_limit
        if entry_limit is None or entry_limit<=0 or entry_limit>=len(order):
            cur_entry_limit = len(order)
            last = ""
        else:
            other_count = sum( [ order[i][1] for i in range(cur_entry_limit, len(order)) ] )
            other_freq = sum( [ order[i][2] for i in range(cur_entry_limit, len(order)) ] )
            last = f", other: {other_count}({round(other_freq,1)}%)"
        out = ", ".join( [f"{order[i][0]}: {order[i][1]}({round(order[i][2],1)}%)" for i in range(cur_entry_limit) ]) + last
        node_stats[node][stat_header] = out

def tallyFreqDict(d1, d2): # Combine two frequency dictionaries. Unused ATM.
    for k, v in d1.items():
        if k in d2:
            d2[k] += v
        else:
            d2[k] = v
    return d2

def parseFreqDict(s): # given a string, parse the frequency dict. Unused ATM.
    d = {}
    if s.strip() == '':
        return d
    fields = s.split(',')
    for x in fields:
        entry = x.split(':')
        val = entry[0].strip()
        count = int(entry[1].split('(')[0].strip())
        d[val] = count
    return d
    

if __name__ == '__main__':
    createNetwork()