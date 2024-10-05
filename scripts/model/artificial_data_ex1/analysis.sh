#!/bin/bash

project_dir=$1
data_type=$2
prompt_type=$3
model=$4

export LANG=C.UTF-8
export PYTHONIOENCODING=utf-8
export PYTHONPATH="$1:$PYTHONPATH"


PYTHONHASHSEED=0 python "${project_dir}/src/artificial_data_ex1/analysis.py" \
        --pred_file="${project_dir}/logs/artificial_data_ex1/${data_type}/${prompt_type}/${model}/test.jsonl" \
        --gold_file="${project_dir}/data/artificial_data_ex1/formatted_data/${data_type}/test.jsonl"






