
def main():
    # some debug code
    #print( extractHeaders('netnames.txt') )
    #print( len(extractMembers( 'clust40.txt',extractHeaders('netnames.txt'))) )

    # example usage
    print( len(decluster(['clust40.txt'], 'netnames.txt')) ) 
    print( len(decluster(['clust40.txt','clust70.txt'], 'netnames.txt')) ) 
    print( len(decluster(['clust40.txt','clust70.txt','clust90.txt'], 'netnames.txt', 'select_members.txt')) )

    # print( len(decluster(['clust90.txt'], 'finalclusters.txt')) ) 

def extractHeaders(cluster_file):
    '''
        Description: Takes a file and extracts fasta headers from it.
            The input is expected to be a cdhit file, but a file with a
            single header on each line is also fine.
            
        Inputs:
        cluster_file - string. Path to a cd_hit cluster file.
        
        Outputs:
        out - list. A list of cluster headers
    '''
    out = []
    with open(cluster_file, 'r') as f:
        for line in f:
            if not line.startswith('>') and not line.strip()=='':
                cur_header = line.split('...')[0].split(' ')[-1].strip()
                if cur_header.startswith('>'):
                    cur_header = cur_header[1:]
                out.append( cur_header )
    return list(set(out))

def extractMembers(cluster_file, cluster_reps):
    '''
        Description: Takes a cluster file from cdhit and extracts all members
            from a cluster if the cluster representative is defined in a list.
            
        Inputs:
        cluster_file - string. Path to a cd_hit cluster file
        cluster_reps - list. A list of cluster headers, whose members should be extracted from the cluster_file
        
        Outputs:
        out - list. A list of cluster headers extracted from the cluster file
    '''
    cur_cluster = None
    clusters = {}
    with open(cluster_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                if not cur_cluster is None:
                    clusters[cur_cluster]=temp
                cur_cluster = None
                temp = []
            else:
                cur_header = line.split('...')[0].split(' ')[-1].strip()
                if cur_header.startswith('>'):
                    cur_header = cur_header[1:]
                temp.append( cur_header )
                if line.strip().endswith('*'):
                    cur_cluster = cur_header
        if not cur_cluster is None:
            clusters[cur_cluster]=temp
    out = []
    for rep in cluster_reps:
        if clusters.get(rep) is not None:
            out.extend(clusters[rep])
    return list(set(out))
    
def decluster(cluster_files, headers_file=None, out_file=None, look_for=None):
    '''
        Description: Takes a series of cluster file from cdhit and extracts all members
            from a cluster if the cluster representative is defined in a list.
            
        Inputs:
        cluster_files - string or list. Path or list of paths to a cd_hit cluster file. To extract members  
                        from successive cdhit files, arrange the filenames from the most condensed to the 
                        least condensied. E.g. 40% -> 70% -> 90%
        headers_file - list. A file containing list of cluster headers, whose members should be extracted from the cluster_file. Use only one of headers_file or look_for.
        out_file -  string. optional. if given, writes all the headers to a file, with each header separated by a new line.
        look_for - list. A list of cluster headers to look for
        
        Outputs:
        out - list. A list of cluster headers extracted from the cluster files
    '''
    if not look_for and headers_file:
        look_for = extractHeaders(headers_file)
        
    if type(cluster_files)!=type([]):
        cluster_files = [cluster_files]
    out = []
    for cluster_file in cluster_files:
        out.extend( extractMembers(cluster_file, out + look_for) )
    out = list(set(out))
    if out_file:
        with open(out_file, 'w') as f:
            for header in out:
                f.write(header+'\n')
    return out

def declusterDict(cluster_files, out_file=None, look_for_dict=None): # takes a dictionary of search target groups, so that all groups can be searched when opening the file just once
    out = look_for_dict
    for cluster_file in cluster_files:
        out = extractMembersDict(cluster_file, out)
    if out_file:
        with open(out_file, 'w') as f:
            for header in out:
                f.write(header+'\n')
    return out

def extractMembersDict(cluster_file, cluster_reps_dict):
    '''
        Description: Takes a cluster file from cdhit and extracts all members
            from a cluster if the cluster representative is defined in a list.
            
        Inputs:
        cluster_file - string. Path to a cd_hit cluster file
        cluster_reps_dict - dict. Dictionary of cluster headers, each with a list of target cluster headers as values whose members should be extracted from the cluster_file.
        
        Outputs:
        out - dict. Dictionary of cluster headers, each with a list of sequence headers found as part of the target clusters.
    '''
    cur_cluster = None
    clusters = {}
    with open(cluster_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                if not cur_cluster is None:
                    clusters[cur_cluster]=temp
                cur_cluster = None
                temp = []
            else:
                cur_header = line.split('...')[0].split(' ')[-1].strip()
                if cur_header.startswith('>'):
                    cur_header = cur_header[1:]
                temp.append( cur_header )
                if line.strip().endswith('*'):
                    cur_cluster = cur_header
        if not cur_cluster is None:
            clusters[cur_cluster]=temp
    out = {}
    for group, cluster_reps in cluster_reps_dict.items():
        out[group] = []
        for rep in cluster_reps:
            if clusters.get(rep) is not None:
                out[group].extend(clusters[rep])
        out[group] = list(set(out[group]))
    return out
    
if __name__=="__main__":
    main()
    
    