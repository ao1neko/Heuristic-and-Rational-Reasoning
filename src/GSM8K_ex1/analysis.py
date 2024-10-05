import argparse
import os

import json
import re


def load_jsonl(file_path):
    log_data = []
    with open(file_path, 'r') as input_json_file:
        for json_data in input_json_file:
            if json != "\n":
                log_data.append(json.loads(json_data))
    return log_data

def get_answer(output:str):
    try:
        output = re.sub(r"\n", "", output)
        regex = re.compile(r"answer is (.+?)\.")
        answer = re.search(regex, output).group(1)
        return answer
    except:
        try: 
            regex = re.compile(r"Therefore.+?has (.+?) ")
            answer = re.search(regex, output).group(1)
            return answer
        except:    
            return None

def main(args):
    number_regex = re.compile(r'\d+',re.DOTALL|re.MULTILINE)
    
    pred_data = load_jsonl(args.pred_file)
    gold_data = load_jsonl(args.gold_file)
    data_length = len(pred_data)
    accuracy = 0
    
    in_redundant_node = 0
    for pred,gold in zip(pred_data,gold_data):
        pred_output = pred["pred_output"]
        redundant_numbers = gold["redundant_numbers"]
        answer = gold["answer"]
        pred_output = re.sub(r"\n", " ", pred_output)
        pred_output = re.sub(r"Context.+", " ", pred_output)
        
        pred_numbers = re.findall(number_regex, pred_output)
        for num in redundant_numbers:
            if num in pred_numbers:
                in_redundant_node += 1
                break
        
        if str(answer) in pred_output:
            print("answer: ", answer)
            print("pred_output: ", pred_output)
            accuracy += 1
    print("in_redundant_percentage: ", in_redundant_node/data_length)
    print("accuracy: ", accuracy/data_length)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--pred_file', default="test1,valid2")
    parser.add_argument('--gold_file', default="test1,valid2")
    parser.add_argument('--data_type', default="flat")
    args = parser.parse_args()
    main(args)