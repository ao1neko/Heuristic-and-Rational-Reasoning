import argparse

import re
from src.artificial_data_ex2.utils import load_jsonl, eval_step


def clean_pred_output(pred_output:str):
    pred_output_list = str(pred_output).split("\n")
    for pred_output_step in pred_output_list:
        if len(pred_output_step.strip()) != 0:
            return pred_output_step
    return None



def main(args):
    pred_data = load_jsonl(args.pred_file)
    gold_data = load_jsonl(args.gold_file)
    shortest_node = 0
    bias_node = 0

    for pred,gold in zip(pred_data,gold_data):
        pred_output = pred["pred_output"]
        gold_output = gold["gold_outputs"][args.depth]
        not_gold_output = gold["not_gold_outputs"][args.depth]
        
        
        pred_output = clean_pred_output(pred_output)
        
        if eval_step(pred_output, gold_output):
            shortest_node += 1
        if eval_step(pred_output, not_gold_output):
            bias_node += 1
    print("shortest_node: ", shortest_node)
    print("not_shortest_node: ", bias_node)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--pred_file', default="test1,valid2")
    parser.add_argument('--gold_file', default="test1,valid2")
    parser.add_argument('--depth', default=3, type=int)
    args = parser.parse_args()
    main(args)


#python analysis.py --input_file "/Users/aoki0903/Desktop/研究室プログラミング/search_capability/logs/formal_language/non_overlap/overlap/text-davinci-003/depth=3_tree=3.jsonl"