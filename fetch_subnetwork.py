
file_template = 'mbl_full_cdhit50_{}-{}clust_{}.txt'
member_suffix = 'membership'
network_suffix = 'network'
node_suffix = 'node_summary'

# when extracting the subnetwork, ensure nodes with these members are included as well, but exclude their neighbours
results_dir = "cluster_extraction/"
base_node_members = {   "B1 cluster":{ "cutoff":(165,173), "nodes":[1]},
                        "B2 cluster":{ "cutoff":(160,165), "nodes":[5957]},
                        "B3 cluster":{ "cutoff":(173,192), "nodes":[2725]}                         
                    }

# target nodes to collect
# allow_neighbours = [str(x) for x in [5957]]
# allow_neighbours = [str(x) for x in []] 
# ignore_neighbours = [str(x) for x in [1]]
# ignore_neighbours = [str(x) for x in []]

network_cutoff = [(160,165),(165,173),(173,192),(192,250),(250,300),(300,350)]
# go through each network
outdir = 'subnetworks/'
    
def main():
    
    for cuts in network_cutoff:
    
        file = results_dir+file_template.format( cuts[0], cuts[1], network_suffix) # network to pull nodes from
        memberfile = results_dir+file_template.format( cuts[0], cuts[1], member_suffix)
        
        outfile = outdir+file_template.format( cuts[0], cuts[1], 'subnetwork')
        
        targets = {}
        for label, info in base_node_members.items():
            tarfile = results_dir+file_template.format( info['cutoff'][0], info['cutoff'][1], member_suffix) # network to pull nodes from
            tarnodes = MatchNodes([ str(x) for x in info['nodes'] ], tarfile, memberfile )
            for x in tarnodes:
                if x not in targets:
                    targets[x] = [label]
                else:
                    targets[x].append(label)
        
        extra_annot = outdir+file_template.format( cuts[0], cuts[1], 'node_info')
        # write extra annotations to file for subnetwork nodes
        with open(extra_annot, 'w') as f:
            f.write('node\tnode_assoc\n')
            for k, v in targets.items():
                f.write(f"{k}\t{','.join(v)}\n")
        
        collected_nodes = {}
        with open(file, 'r') as f: # determine nodes to include
            for line in f:
                row = line.split('\t')
                n1, n2 = row[0], row[1]
                # if (n1 in allow_neighbours or n2 in allow_neighbours) or ((n1 in ignore_neighbours and n2 in ignore_neighbours)):
                if (n1 in targets or n2 in targets):
                    collected_nodes[n1] = True
                    collected_nodes[n2] = True
       
        with open(file, 'r') as f: # fetch all interconnecting edges between selected nodes
            with open(outfile, 'w') as fo:
                fo.write(next(f))
                for line in f:
                    row = line.split('\t')
                    n1, n2 = row[0], row[1]
                    if n1=="" or n2=="":
                        continue
                    if n1 in collected_nodes and n2 in collected_nodes:
                        fo.write(line)

def MatchNodes(source_nodes, source_members, target_members):
    fetch = GetMemberByNode(source_nodes, source_members)
    
    new_nodes = {}
    with open(target_members, 'r') as f:
        for line in f:
            row = line.split('\t')
            node = row[0].strip()
            member = row[1].strip()
            if member in fetch and node not in new_nodes:
                new_nodes[node] = True
                
    return list(new_nodes.keys())

def GetMemberByNode(source_nodes, source_members):
    fetch = {}
    with open(source_members, 'r') as f:
        for line in f:
            row = line.split('\t')
            node = row[0].strip()
            member = row[1].strip()
            if node in source_nodes:
                fetch[member] = True
    return fetch
    
if __name__ == "__main__":
    main()