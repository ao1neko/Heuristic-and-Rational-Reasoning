#!/bin/bash

project_dir=$1
data_type=$2
prompt_type=$3
model=$4
depth=$5

export LANG=C.UTF-8
export PYTHONIOENCODING=utf-8
export PYTHONPATH="$1:$PYTHONPATH"


PYTHONHASHSEED=0 python "${project_dir}/src/artificial_data_ex2/analysis_clean.py" \
        --pred_file="${project_dir}/logs/artificial_data_ex2/${data_type}/${prompt_type}/${model}/${depth}/test.jsonl" \
        --gold_file="${project_dir}/data/artificial_data_ex2/formatted_data/${data_type}/test.jsonl" \
        --depth="${depth}"






