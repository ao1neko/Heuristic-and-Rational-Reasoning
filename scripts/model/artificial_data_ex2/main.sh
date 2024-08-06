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

#model="gpt-3.5-turbo"
#model="gpt-4"

# ./main_chat.sh /Users/aoki0903/Desktop/研究室プログラミング/search_capability flat flat gpt-3.5-turbo 0
# ./main_chat.sh /Users/aoki0903/Desktop/研究室プログラミング/search_capability overlap flat gpt-3.5-turbo 0