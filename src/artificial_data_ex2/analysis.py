import argparse
import re

from src.artificial_data_ex2.utils import load_jsonl, eval_step, get_answer

def main(args):
    pred_data = load_jsonl(args.pred_file)
    gold_data = load_jsonl(args.gold_file)
    shortest_node = 0
    heuristic_node = 0
    distract_node = 0
    accuracy = 0
    regex = re.compile(r"So, (.+?) has")

    
    for pred,gold in zip(pred_data,gold_data):
        distract_num = 8
        pred_output = pred["pred_output"]
        gold_output = gold["gold_outputs"][args.depth]
        heuristic_outputs = gold["heuristic_outputs"][:args.depth+1]
        #distract_outputs = gold["distract_outputs"][(args.depth*distract_num):((args.depth+1)*distract_num)]
        distract_outputs = gold["distract_outputs"][:((args.depth+1)*distract_num)]
        
        
        if eval_step(pred_output, gold_output):
            shortest_node += 1
        #for not_gold_output in not_gold_outputs:
        for heuristic_output in heuristic_outputs:
            if eval_step(pred_output, heuristic_output):
                heuristic_node += 1
                break

        for distract_output in distract_outputs:
            if eval_step(pred_output, distract_output):
                distract_node += 1
                break
        #else:
        #   print("pred_output: ", pred_output)
        #    print("gold_output: ", gold_output)
        #    print("heuristic_output: ", heuristic_output)
        #    print("################################################################")
            #break
    print("shortest_node: ", shortest_node)
    print("heuristic_node: ", heuristic_node)
    print("distract_node: ", distract_node)
    print(1)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--pred_file', default="test1,valid2")
    parser.add_argument('--gold_file', default="test1,valid2")
    parser.add_argument('--depth', default=3, type=int)
    args = parser.parse_args()
    main(args)


#python analysis.py --input_file "/Users/aoki0903/Desktop/研究室プログラミング/search_capability/logs/formal_language/non_overlap/overlap/text-davinci-003/depth=3_tree=3.jsonl"