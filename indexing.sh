#!/usr/bin/env bash

export SPLADE_CONFIG_NAME="config_splade++_cocondenser_ensembledistil"
python3 -m splade.index \
  init_dict.model_type_or_dir=naver/splade-cocondenser-ensembledistil \
  config.pretrained_no_yamlconfig=true \
  config.index_dir="index/2020index" \
  config.out_dir="index/2020outputs" \
  data.COLLECTION_PATH="2020data"
