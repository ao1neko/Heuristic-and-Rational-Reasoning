import argparse
import os

import json
import re
from src.classes.executor_class import GPT
from src.GSM8K_ex1.utils import read_jsonl_file
from tqdm import tqdm
from pathlib import Path

def main(args):
    inputs, _, _ = read_jsonl_file(args.input_file)
    #inputs = inputs[:2]

    prompt = [
    {
      "role": "system",
      "content": [
        {
          "text": "Answer the context question according to the following example.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Leo's assignment was divided into three parts. Weng earns $12 an hour for babysitting. It took Leo twice as long to finish the second part. Yesterday, she just did 50 minutes of babysitting. \nQuestion: How much did Weng earn?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Weng earns 12/60 = 0.2 per minute.\nWorking 50 minutes, she earned 0.2 x 50 = 10. \nThe final answer is 10.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Alice is saving money for a new wallet which costs $2000. Bettys parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents.\nQuestion: How much more money does Betty need to buy the wallet?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "In the beginning, Betty has only 100 / 2 = 50.\nBetty's grandparents gave her 15 * 2 = 30.\nThis means, Betty needs 100 - 50 - 30 - 15 = 5 more.\nThe final answer is 5.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Julie is reading a 120-page book. Yesterday, Julie was able to read 12 pages and today, she read twice as many pages as yesterday. Julie' s mother makes $18.00 an hour. \nQuestion: How many pages are left to be read?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Julie read 12 x 2 = <<12*2=24>>24 pages today.\nSo she was able to read a total of 12 + 24 = 36 pages since yesterday.\nThere are 120 - 36 = 84 pages left to be read.\nSince she wants to read half of the remaining pages tomorrow, then she should read 84/2 = 42 pages.\nThe final answer is 42.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: James writes a 2-page letter to 4 different friends, lived in America, twice a week.  James writes a 3-page letter to 2 different friends, lived in Japan,  twice a week.  \nQuestion: How many pages does James write each friend lived in Japan at one time?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "He writes each friend 3*2=6 pages a week.\nSo he writes 6*2=12 pages every week.\nThat means he writes 12*52=624 pages a year.\nThe final answer is 624.",
          "type": "text"
        }
      ]
    }
  ]
    module = GPT(prompt=prompt, model=args.model)

    os.makedirs(Path(args.output_file).parent, exist_ok=True)
    with open(args.output_file, "w") as f, open(args.output_json_file, "w") as jf:
        for index in tqdm(range(0, len(inputs))):
            response = module.send(context=inputs[index],answers=[],max_tokens=200)
            
            json_data = {
                "input": inputs[index],
                "pred_output": response,
            }
            jf.write(json.dumps((json_data)))
            jf.write("\n")
            f.write("Context:\n")
            f.write(inputs[index]+"\n")
            f.write("pred_outputs:\n")
            f.write(response+"\n")
            f.write("------------------\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input_file', default="test1,valid2")
    parser.add_argument('--output_file', default="save/test")
    parser.add_argument('--output_json_file', default="save/test")
    parser.add_argument('--model', default="")
    args = parser.parse_args()
    main(args)


