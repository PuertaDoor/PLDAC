with open("2020data/2020qrels.tsv", "r") as source:
    ids = open("2020data/mini/id_numb.tsv", "r").read().splitlines()
    qrel_splade = open("2020data/mini/qrels_splade.tsv", "w")
    for line in source:
        tmp = line.rstrip().split('\t')
        for tuple in ids:
            tmp2 = tuple.rstrip().split('\t')
            if len(tmp2)>1:
                if tmp2[1] == tmp[1]:
                    num_id = tmp2[0]
                    qrel_splade.write(f"{tmp[0]}" + "\t" + f"{num_id}" + "\t" + f"{tmp[2]}" + "\t" + f"{tmp[3]}" + "\n")
    qrel_splade.close()
