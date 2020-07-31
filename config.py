#                   ***************************************
#                   ******** Manual Configurations ********
#                   ***************************************

# ----------------------------------------------------------------
# --------      Part 1, meta-network generation settings      ----------
# ----------------------------------------------------------------
# 1. What is the path to the folder containing the BLAST result files ? Please end all folders with a single slash ('/').
blast_results_path = 'C:/Users/Tokuriki Lab/Documents/Sync/Projects/MBL SSN 2020/mbl_cdhit50_all_by_all/'


# 2. Which files in the input folder should be used for this analysis ? Setting None will use all files in the input folder.
# blast_results_files = ['b1_all_by_all.txt','b2_vs_b1_all_blast.txt','b2_vs_b1_all_as_subject.txt']
blast_results_files = None

# 3. Which columns (1st column is 0, 2nd is 1, etc) in the blast files contain the following information ?
#    Please ensure this is true for all files given as input.
query_col = 0
subject_col = 1
bitscore_col = 3

# Obsolete : clustering thresholds now provided directly through command line
# 4. At what bitscore threshold should sequences be grouped together into a metanode ?
# metanode_bitscore_range = range(100,310,10) 

# 5. At what bitscore threshold should edge connections be ignored for the network ?
# fixed_min_bitscore = None
# bitscore_gap = 10


# 6. Enter the path to the file used to limit the sequences used in the analysis ? Only sequence IDs present in the file will be used in the analysis.
#    If set to None, ther filter is ignored.
#    The file should be formatted to have a single sequence ID on each line
filter_path = 'input/filters/'
filter_files = []
# filter_files = ['b1_subgroup_all_reps.txt']

# 7. What should the output be named? The label given should only describe the input data, as the bitscore cut-offs and other information will be added as suffixes automatically.
output_label = 'mbl_full_cdhit50'
# output_label = 'b1_subgroup'

# 8. Where should the output be placed ? This will create a directory relative to the scripts running location.
# output_dir = 'result_tiered/'
# output_dir = 'cluster_extraction/'
output_dir = 'metaSSN_v4_test/'
# use_old_metanodes = True # use old if found

# 9. Out put member names can be remapped, supply a mapping file with the old name in the first column and the new name in the second
#    names not found in the file will be left as is.
mapping_path = 'C:/Users/Tokuriki Lab/Documents/Sync/Projects/MBL SSN 2020/sequences/'
member_name_mapping = []

# ----------------------------------------------------------------
# ------- Part 2, resolving sequence clustering, OPTIONAL --------
# ----------------------------------------------------------------
# 1. Should member sequences in the metanodes be analysed for cluster members ? Only applicable if each member sequence is the representative of a cluster of sequences, 
#    and should be set to False otherwise.
# analyze_clustering = True
# use_old_clustering = True

# 2. What is the path to the folder containing clustering information ?
cluster_info_path = 'C:/Users/Tokuriki Lab/Documents/Sync/Projects/MBL SSN 2020/sequences/'

# 3. Describe each file in the input folder using the following Dictionary.
#    Each top level key should be the name of the file, and the value should be a dictionary specifying if the file is 1) a 'cdhit' cluster or a 'table', 
#    2) a label to give data extracted from this clustering, 3) the table delimiter, 4) the key column of the table for matching sequence IDs, 
#    5) the column in the table that contains member information, and 6) the delimiter that separates cluster members in the table's string.
#    Properties 3-6 are for tables only and can be set to None for cdhit files. Properties 4-5 should be given with 0 as the 1st column, 1 as the 2nd, etc.
#    For heirarchical clustering of cdhit files, only the lowest identity file needs to be assigned, the remainder should be provided below.

# label currently unused, doesn't make sense, since clustering may not necessarily mean distinct datasets
cluster_file_info = {
                        'mbl_cdhit50.clstr': {'format':'cdhit', 'delim':None, 'key_col':None, 'member_col':None, 'member_delim':None}
                        # 'B1_230_to_300_cdhit.clstr': {'format':'cdhit', 'label':'metagenome', 'delim':None, 'key_col':None, 'member_col':None, 'member_delim':None},
                        # 'CARD_b1_cdhit70.clstr': {'format':'cdhit', 'label':'B1', 'delim':None, 'key_col':None, 'member_col':None, 'member_delim':None},
                        # 'CARD_b2_cdhit70.clstr': {'format':'cdhit', 'label':'B2', 'delim':None, 'key_col':None, 'member_col':None, 'member_delim':None},
                        # 'uniref50_IPR001279.tab': {'format':'table', 'label':'uniprot', 'delim':'\t', 'key_col':0, 'member_col':4, 'member_delim':';'}
                    }

# 4. For cdhit based clustering, describe heirarchical clustering, if any. Use a dictionary where the key is the clustering with the lowest identity, and 
#    the value is a list of the other files in the heirarchy in ascending order of identity cut-off. 
#    If not, give None as the input.
# example
# cdhit_heirarchy = {  '40%.clstr': ['70%.clstr','90%.clstr'] }
cdhit_heirarchy = {'mbl_cdhit50.clstr': ['mbl_cdhit70.clstr','mbl_cdhit90.clstr'] }

# ----------------------------------------------------------------
# -------       Part 3, extra annotation, OPTIONAL        --------
# ----------------------------------------------------------------
# 1. Would you like to add extra annotations ?
# annot_metanodes = True

# 2. Provide the path to the folder containing the annotation files.
annot_path = 'input/annot/'

# 3. Provide a list of files to annotate by membership count. Each entry should be a dictionary 
#    that specifies the filename, the annotation label and the level at which the annotations should be applied (metanode members vs all sequences in metanode)
#    Each file should be a series of sequence IDs separated by new lines. The IDs should be non-redundant.
#    NOTE: the same file may not work for both 'member' and 'sequence' level extractions, since representative members may have different names than at the individual sequence level
#          such as UniRef vs UniProt IDs
membership_count_annot = [
                            {'files':'b1_refs.txt','id_col':0,'data_col':None,'delim':'\t','label':'CARD B1','level':'sequence'},
                            {'files':'b2_refs.txt','id_col':0,'data_col':None,'delim':'\t','label':'CARD B2','level':'sequence'},
                            {'files':'b3_refs.txt','id_col':0,'data_col':None,'delim':'\t','label':'CARD B3','level':'sequence'},
                            {'files':'mbl_swissprot_acc.txt','id_col':0,'data_col':None,'delim':'\t','label':'SwissProt','level':'sequence'},
                            {'files':'mbl_uniprot_acc.txt','id_col':0,'data_col':None,'delim':'\t','label':'UniProt','level':'sequence'},
                            {'files':'jgi_headers.txt','id_col':0,'data_col':None,'delim':'\t','label':'JGI','level':'sequence'}
                            # {'files':'b1_refs.txt','id_col':0,'data_col':None,'delim':'\t','label':'known B1','level':'member'},
                            # {'files':'b1_refs.txt','id_col':0,'data_col':None,'delim':'\t','label':'known B1','level':'sequence'},
                            # {'files':'ipr001279_acc.txt','id_col':0,'data_col':None,'delim':'\t','label':'UniProt','level':'sequence'},
                            # {'files':'JGI_b1_230-300aa_headers.txt','id_col':0,'data_col':None,'delim':'\t','label':'JGI','level':'sequence'}
                         ]                    
                        
# 4. Provide a list of files to annotate by frequency of certain traits (genus, kingdom, etc). Each entry should be a dictionary 
#    that specifies the file name, the column of the sequence id, the column of the data, the file delimiter, the annotation label and the level at which the annotations 
#    should be applied (metanode members vs all sequences in metanode)
#    Each file should be a tab separated file with the sequence ID in the first column, and the trait in the second column.
membership_freq_annot = [
                            # {'files':'b1_active_sites.txt','id_col':0,'data_col':1,'delim':'\t','label':'active_site','level':'member','highest_entries':3},
                            # {'files':'b1_active_sites.txt','id_col':0,'data_col':1,'delim':'\t','label':'active_site','level':'member','highest_entries':3},
                            {'files':'ipr001279_org_annot_filled.txt','id_col':0,'data_col':2,'delim':'\t','label':'genus','level':'sequence','highest_entries':5},
                            {'files':['B1_activesite.txt'],'id_col':0,'data_col':1,'delim':'\t','label':'B1_activesite','level':'sequence','highest_entries':3},
                            {'files':['B2_activesite.txt'],'id_col':0,'data_col':1,'delim':'\t','label':'B2_activesite','level':'sequence','highest_entries':3},
                            {'files':['B3_activesite.txt'],'id_col':0,'data_col':1,'delim':'\t','label':'B3_activesite','level':'sequence','highest_entries':3},
                            {'files':['B1_200-350aa_activesite.txt'],'id_col':0,'data_col':1,'delim':'\t','label':'B1_200-350aa_activesite','level':'sequence','highest_entries':3},
                            {'files':['B2_200-350aa_activesite.txt'],'id_col':0,'data_col':1,'delim':'\t','label':'B2_200-350aa_activesite','level':'sequence','highest_entries':3},
                            {'files':['B3_200-350aa_activesite.txt'],'id_col':0,'data_col':1,'delim':'\t','label':'B3_200-350aa_activesite','level':'sequence','highest_entries':3},
                            {'files':['B1_MSA_inclusion.txt'],'id_col':0,'data_col':1,'delim':'\t','label':'B1_200-350aa_MSA_inclusion','level':'sequence','highest_entries':3},
                            {'files':['B2_MSA_inclusion.txt'],'id_col':0,'data_col':1,'delim':'\t','label':'B2_200-350aa_MSA_inclusion','level':'sequence','highest_entries':3},
                            {'files':['B3_MSA_inclusion.txt'],'id_col':0,'data_col':1,'delim':'\t','label':'B3_200-350aa_MSA_inclusion','level':'sequence','highest_entries':3}
                        ]

# 5. Unique labels
membership_label =  [
                        {'files':'b1_name.txt','id_col':1,'data_col':2 ,'delim':'\t', 'label':'known B1 families', 'level':'sequence'},
                        {'files':'b2_name.txt','id_col':1,'data_col':2 ,'delim':'\t', 'label':'known B2 families', 'level':'sequence'},
                        {'files':'b3_name.txt','id_col':1,'data_col':2 ,'delim':'\t', 'label':'known B3 families', 'level':'sequence'},
                        # {'files':'b1_family_label.txt','id_col':0,'data_col':1 ,'delim':'\t', 'label':'known B1 families', 'level':'member'}
                    ]     

# 6. Numerical distribution
membership_dist_annot = [
                            # {'files':['ipr001279_length.txt', 'JGI_b1_230-300aa_headers+length.txt'],'id_col':0,'data_col':1,'delim':'\t','label':'length_dist','level':'sequence'}
                            {'files':'mbl_lengths.txt','id_col':0,'data_col':1,'delim':'\t','label':'length_dist','level':'sequence'}
                        ] 
            

# 7. link nodes at higher cut-offs to those observed at lower ones. Make sure the file is a lower cut-off than the currently set metanode bitscores, or else the results
#    will not make any sense. It also doesn't need to be from the same set of analysis, since node numbering is arbitrary so long as the clustering is correct. 
#    level should always be member.
membership_lower_node = [
                            # {'files':'b1_ssn_50min_115clust_meta-node_members.txt','id_col':1,'data_col':0 ,'delim':'\t', 'label':'115clust node', 'level':'member', 'bitscore':115}
                        ]  