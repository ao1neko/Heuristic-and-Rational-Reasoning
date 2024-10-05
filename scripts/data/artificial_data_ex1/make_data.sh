#!/bin/bash

project_dir=$1


export LANG=C.UTF-8
export PYTHONIOENCODING=utf-8
export PYTHONPATH="$1:$PYTHONPATH"


PYTHONHASHSEED=0 python "${project_dir}/src/data/artificial_data_ex1/make_data.py" \
    --output_dir="${project_dir}/data/artificial_data_ex1/formatted_data/" \

echo "formatted test.jsonl"

