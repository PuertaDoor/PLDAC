#!/usr/bin/env bash

export SPLADE_CONFIG_NAME="config_splade++_cocondenser_ensembledistil"


rm -dR index/2020mini_index
rm -dR index/2020mini_outputs
mkdir index/2020mini_index
mkdir index/2020mini_outputs
python3 -m splade.index \
  init_dict.model_type_or_dir=naver/splade-cocondenser-ensembledistil \
  config.train_batch_size=128 \
  config.eval_batch_size=500 \
  config.index_retrieve_batch_size=8 \
  config.pretrained_no_yamlconfig=true \
  config.index_dir=index/2020mini_index \
  config.out_dir=index/2020mini_outputs \
  data.COLLECTION_PATH=2020data/mini
