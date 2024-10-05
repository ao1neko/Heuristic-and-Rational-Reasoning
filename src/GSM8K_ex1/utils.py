from pathlib import Path
from typing import List, Dict, Tuple
import re
import json
import math


def read_jsonl_file(input_file: Path):
    inputs = []
    answers = []
    redundant_numbers = []
    with open(input_file, 'r') as input_json_file:
        for json_data in input_json_file:
            if json_data != "\n":
                json_data = json.loads(json_data)
                inputs.append(json_data["input"])
                answers.append(float(clean_number(json_data["answer"])))
                redundant_numbers.append(json_data["redundant_numbers"])
    return (inputs,answers,redundant_numbers)

def clean_number(number):
    number = number.replace(",","")
    return number

def eval_answer(pred_answer, gold_answer):
    if math.isclose(pred_answer,gold_answer):
        return True
    return False


def eval_answer_and_steps(left_args, redundant_numbers,pred_answer, gold_answer):
    number_regex = re.compile(r'\d+')
    
    if not eval_answer(pred_answer, gold_answer):
        return False
    else:
        pred_numbers = list(set(re.findall(number_regex, " , ".join(left_args))))
        
        for number in pred_numbers:
            if number in redundant_numbers:
                return False
        return True
    
def eval_equations(left_args, right_args):
    for equation,answer in zip(left_args,right_args):
        try:
            if not math.isclose(float(eval(equation)),float(answer)):
                return False
        except:
            print(equation,answer)
    return True