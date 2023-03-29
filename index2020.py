# FROM NAM LE HAI
# GITHUB : https://github.com/nam685/

from tqdm import tqdm
import pyterrier as pt
pt.init()

def trec2020_generate():
    with open("2020data/2020docs.tsv", 'r') as corpusfile:
        for l in tqdm(corpusfile,total=38622439):
            doc_id, text = l.split("\t",1)
            if len(text) > 0:
                yield {'docno' : doc_id, 'text' : text}

iter_indexer = pt.IterDictIndexer("./index", meta=['docno'])
print("Indexing 38622439 TREC 2020 docs")
indexref = iter_indexer.index(trec2020_generate())
