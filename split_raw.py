# INSPIRED FROM NAM LE HAI

import sys
from pathlib import Path

if len(sys.argv)!=2:
    print("python split_raw <repo>")
    exit(1)
name = sys.argv[1]

size = 2048000
cpt = 0
i = 0
with open(f"{name}/raw.tsv",'r') as source:
    ids = open("2020data/id_numb.tsv", "w")
    for line in source:
        line_sp = line.rstrip().split('\t')
        id = line_sp[0]
        ids.write(f"{cpt}" + "\t" + f"{id}" + "\n")
        if cpt%size==0:
            try:
                dest.close()
            except:
                None
            Path(name + "/raw/" + name + "_" + str(cpt)).mkdir(parents=True, exist_ok=True)
            dest = open(f"{name}/raw/{name}_{cpt}/raw.tsv",'w')
        if len(line_sp) > 1:
            passage = line_sp[1]
        else:
            passage = ""
        dest.write(f"{cpt}" + "\t" + f"{passage}" + "\n")
        cpt += 1
    ids.close()
