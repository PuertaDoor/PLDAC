# INSPIRED FROM NAM LE HAI

import sys

if len(sys.argv)!=2:
    print("python encode_onefile <repo>")
    exit(1)
name = sys.argv[1]


cpt = 0
with open(f"{name}/first_raw.tsv",'r') as source:
    ids = open(f"{name}/id_numb.tsv", "w")
    dest = open(f"{name}/raw.tsv",'w')
    for line in source:
        line_sp = line.rstrip().split('\t')
        id = line_sp[0]
        ids.write(f"{cpt}" + "\t" + f"{id}" + "\n")
        if len(line_sp) > 1:
            passage = line_sp[1]
        else:
            passage = ""
        dest.write(f"{cpt}" + "\t" + f"{passage}" + "\n")
        cpt += 1
    ids.close()
    dest.close()
