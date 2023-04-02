# FROM NAM LE HAI
# GITHUB : https://github.com/nam685/

from tqdm import tqdm
import os
import pyterrier as pt
pt.init()

files = os.listdir('2020data/raw')

def trec2020_generate(file):
    with open(f"2020data/raw/{file}/raw.tsv", 'r') as corpusfile:
        for l in tqdm(corpusfile,total=2048000):
            doc_id, text = l.split("\t",1)
            if len(text) > 0:
                yield {'docno' : doc_id, 'text' : text}

for file in files:
    os.mkdir(f"./index/2020index/{file}")
    iter_indexer = pt.IterDictIndexer(f"./index/2020index/{file}", meta=['docno'])
    print("Indexing 2048000 TREC 2020 docs")
    indexref = iter_indexer.index(trec2020_generate(file))