#!/bin/bash

project_dir=$1


export LANG=C.UTF-8
export PYTHONIOENCODING=utf-8
export PYTHONPATH="$1:$PYTHONPATH"


PYTHONHASHSEED=0 python "${project_dir}/src/data/artificial_data_ex2/make_data.py" \
    --output_file="${project_dir}/data/artificial_data_ex2/formatted_data/flat/test.jsonl" \
    --data_type="flat" \

PYTHONHASHSEED=0 python "${project_dir}/src/data/artificial_data_ex2/make_data.py" \
    --output_file="${project_dir}/data/artificial_data_ex2/formatted_data/overlap/test.jsonl" \
    --data_type="overlap" \

PYTHONHASHSEED=0 python "${project_dir}/src/data/artificial_data_ex2/make_data.py" \
    --output_file="${project_dir}/data/artificial_data_ex2/formatted_data/negative/test.jsonl" \
    --data_type="negative" \

PYTHONHASHSEED=0 python "${project_dir}/src/data/artificial_data_ex2/make_data.py" \
    --output_file="${project_dir}/data/artificial_data_ex2/formatted_data/position/test.jsonl" \
    --data_type="position" \

echo "formatted test.jsonl"

# ./make_data.sh /Users/aoki0903/Desktop/研究室プログラミング/search_capability