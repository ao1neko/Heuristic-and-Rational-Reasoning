#!/bin/bash

project_dir=$1
data_type=$2
prompt_type=$3
model=$4
depth=$5

export LANG=C.UTF-8
export PYTHONIOENCODING=utf-8
export PYTHONPATH="$1:$PYTHONPATH"



PYTHONHASHSEED=0 python "${project_dir}/src/artificial_data_ex2/main.py" \
        --input_file="${project_dir}/data/artificial_data_ex2/formatted_data/${data_type}/test.jsonl" \
        --output_file="${project_dir}/logs/artificial_data_ex2/${data_type}/${prompt_type}/${model}/${depth}/test.txt" \
        --output_json_file="${project_dir}/logs/artificial_data_ex2/${data_type}/${prompt_type}/${model}/${depth}/test.jsonl" \
        --prompt_type="${prompt_type}" \
        --model=${model} \
        --depth="${depth}" \





