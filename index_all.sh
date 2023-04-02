#!/usr/bin/env bash

#SBATCH --job-name=wapo_splade_index
#SBATCH --nodes=1
#SBATCH --gpus-per-node=1
#SBATCH --time=5000

export SPLADE_CONFIG_NAME="config_splade++_cocondenser_ensembledistil"

file="all"

rm -dR index/2020index/$file
rm -dR index/2020outputs/$file
mkdir index/2020index/$file
mkdir index/2020outputs/$file
python3 -m splade.index \
  init_dict.model_type_or_dir=naver/splade-cocondenser-ensembledistil \
  config.pretrained_no_yamlconfig=true \
  config.index_dir="index/2020index/$file" \
  config.out_dir="index/2020outputs/$file" \
  data.COLLECTION_PATH=2020data/$file