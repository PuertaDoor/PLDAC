#!/usr/bin/env bash
pip install --upgrade ir_datasets

# FOR 2020 DATA
DIRECTORY="2020data"

if [ ! -d "$DIRECTORY" ]; then
  mkdir $DIRECTORY
fi

ir_datasets export trec-cast/v1/2020 queries --format tsv > $DIRECTORY/2020queries.tsv
ir_datasets export trec-cast/v1/2020 docs --format tsv > $DIRECTORY/2020docs.tsv
ir_datasets export trec-cast/v1/2020 qrels --format tsv > $DIRECTORY/2020qrels.tsv


# FOR 2021 DATA
DIRECTORY="2021data"

if [ ! -d "$DIRECTORY" ]; then
  mkdir $DIRECTORY
fi

ir_datasets export kilt/codec queries --format tsv --fields query_id, query > $DIRECTORY/kilt_queries.tsv
ir_datasets export kilt/codec docs --format tsv --fields doc_id, text > $DIRECTORY/kilt_docs.tsv
ir_datasets export kilt/codec qrels --format tsv > $DIRECTORY/kilt_qrels.tsv

ir_datasets export msmarco-document/trec-dl-2020 queries --format tsv > $DIRECTORY/msmarco_queries.tsv
ir_datasets export msmarco-document/trec-dl-2020 docs --format tsv --fields doc_id, body > $DIRECTORY/msmarco_docs.tsv
ir_datasets export msmarco-document/trec-dl-2020 qrels --format tsv > $DIRECTORY/msmarco_docs.tsv

# WAPO IS A PRIVATE DATASET, CONTACT THE NIST TO GET THE DATASET
