# INSPIRED FROM NAM LE HAI

import sys
from pathlib import Path

if len(sys.argv)!=2:
    print("python split_raw <repo>")
    exit(1)
name = sys.argv[1]

size = 2048000
cpt = 0
with open(f"{name}/raw.tsv",'r') as source:
    for line in source:
        i = line.rstrip().split('\t')[0]
        if cpt%size==0:
            try:
                dest.close()
            except:
                None
            Path(name + "/raw/" + name + "_" + str(cpt)).mkdir(parents=True, exist_ok=True)
            dest = open(f"{name}/raw/{name}_{cpt}/raw.tsv",'w')
        dest.write(line)
        cpt += 1