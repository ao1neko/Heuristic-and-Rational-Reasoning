#!/bin/bash

project_dir=$1
data_type=$2
model="PaLM2"

export LANG=C.UTF-8
export PYTHONIOENCODING=utf-8
export PYTHONPATH="$1:$PYTHONPATH"



PYTHONHASHSEED=0 python "${project_dir}/src/GSM8K_ex1/main_palm2.py" \
        --input_file="${project_dir}/data/GSM8K_ex1/formatted_data/${data_type}.jsonl" \
        --output_file="${project_dir}/logs/GSM8K_ex1/${model}/${data_type}.txt" \
        --output_json_file="${project_dir}/logs/GSM8K_ex1/${model}/${data_type}.jsonl"



