#!/bin/bash

project_dir=$1

export LANG=C.UTF-8
export PYTHONIOENCODING=utf-8
export PYTHONPATH="$1:$PYTHONPATH"

for data_type in "flat" "overlap" "negative" "not_negative" "position" 
do
    PYTHONHASHSEED=0 python "${project_dir}/src/data/GSM8K_ex1/make_data.py" \
        --input_file="${project_dir}/data/GSM8K/test.jsonl" \
        --output_dir="${project_dir}/data/GSM8K_ex1/formatted_data/" \
        --data_type="${data_type}" \

    echo "formatted ${data_type}.jsonl"
done