
def map( memberfile, mapfile):
    m = {}
    header = ""
    with open(memberfile, 'r') as f:
        header = next(f)
        for line in f:
            row = line.split('\t')
            m[row[1].strip()] = row[0].strip()
            
    with open(mapfile, 'r') as f: # old name on first column, new name on second, expect no header
        for line in f:
            row = line.split('\t')
            old = row[0].strip()
            new = row[1].strip()
            if old in m:
                if new in m:
                    print(f'Warning: The header \'{new}\' is not unique.')
                    return False
                m[new] = m[old]
                del m[old]
                
    with open(memberfile, 'w') as f:
        f.write(header)
        for member, node in m.items():
            f.write(f"{node}\t{member}\n")
                
                