# FROM NAM LE HAI
# github.com/nam685/cosplade

import json
import pytrec_eval
import sys

if len(sys.argv)!=3:
    print("python eval <run> <qrel>")
    exit(1)
runstr = sys.argv[1]
qrelstr = sys.argv[2]

with open(f"{runstr}.json", "r") as runf:
    with open(f"{qrelstr}.json","r") as qrelf:
        run_obj = json.load(runf)
        if qrelstr == "qr21":
            run_obj = cut(run_obj, 500)

        qrel = json.load(qrelf)

        evaluator = pytrec_eval.RelevanceEvaluator(qrel, {'recall', 'map_cut', 'recip_rank', 'ndcg_cut'})
        res = evaluator.evaluate(run_obj)
        print(json.dumps(res, indent=1))
