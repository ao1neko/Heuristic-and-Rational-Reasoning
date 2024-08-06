#!/bin/bash

project_dir=$1
data_type=$2
model=$3

export LANG=C.UTF-8
export PYTHONIOENCODING=utf-8
export PYTHONPATH="$1:$PYTHONPATH"


PYTHONHASHSEED=0 python "${project_dir}/src/GSM8K_ex1/main.py" \
        --input_file="${project_dir}/data/GSM8K_ex1/formatted_data/${data_type}.jsonl" \
        --output_file="${project_dir}/logs/GSM8K_ex1/${model}/${data_type}.txt" \
        --output_json_file="${project_dir}/logs/GSM8K_ex1/${model}/${data_type}.jsonl" \
        --model=${model} \


#./main.sh /Users/aoki0903/Desktop/研究室プログラミング/search_capability flat gpt-3.5-turbo
