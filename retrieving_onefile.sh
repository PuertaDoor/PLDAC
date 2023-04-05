#!/usr/bin/env bash

export SPLADE_CONFIG_NAME="config_splade++_cocondenser_ensembledistil"

rm -dR retrieve/2020mini
mkdir retrieve/2020mini
python3 -m splade.retrieve \
  init_dict.model_type_or_dir=naver/splade-cocondenser-ensembledistil \
  config.pretrained_no_yamlconfig=true \
  config.index_dir=index/2020mini_index \
  config.out_dir=retrieve/2020mini \
  data.Q_COLLECTION_PATH=2020data/2020queries_judged \
  data.EVAL_QREL_PATH=2020data/mini/TREC_qrels_splade.json
