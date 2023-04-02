#!/usr/bin/env bash

export SPLADE_CONFIG_NAME="config_splade++_cocondenser_ensembledistil"

files=$(ls 2020data/raw)

for file in $files
do
    rm -dR index/2020index/$file
    rm -dR index/2020outputs/$file
    mkdir index/2020index/$file
    mkdir index/2020outputs/$file
    python3 -m splade.index \
      init_dict.model_type_or_dir=naver/splade-cocondenser-ensembledistil \
      config.train_batch_size=128 \
      config.eval_batch_size=500 \
      config.index_retrieve_batch_size=24 \
      config.pretrained_no_yamlconfig=true \
      config.index_dir="index/2020index/$file" \
      config.out_dir="index/2020outputs/$file" \
      data.COLLECTION_PATH=2020data/raw/$file
done
