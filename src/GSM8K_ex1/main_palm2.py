import argparse
import os
import google.generativeai as genai

import json
from pathlib import Path
from tqdm import tqdm
from src.GSM8K_ex1.utils import read_jsonl_file
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
)  # for exponential backoff

@retry(wait=wait_fixed(30), stop=stop_after_attempt(3))
def send(prompt:str):
    response = str(genai.generate_text(prompt=prompt,temperature=0,top_p=1.0,max_output_tokens=256).result)
    return response
    

def main(args):
    inputs, outputs, answers = read_jsonl_file(args.input_file)
    inputs = [x + "\nAnswer:\n" for x in inputs]
    #inputs = inputs[:2]

    prompt="Answer the context question according to the following example.\n\nContext: Leo's assignment was divided into three parts. Weng earns $12 an hour for babysitting. It took Leo twice as long to finish the second part. Yesterday, she just did 50 minutes of babysitting. \nQuestion: How much did Weng earn?\nAnswer:\nWeng earns 12/60 = 0.2 per minute.\nWorking 50 minutes, she earned 0.2 x 50 = 10. \nThe final answer is 10.\n\nContext: Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Alice is saving money for a new wallet which costs $2000. Bettys parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents.\nQuestion: How much more money does Betty need to buy the wallet?\nAnswer:\nIn the beginning, Betty has only 100 / 2 = 50.\nBetty's grandparents gave her 15 * 2 = 30.\nThis means, Betty needs 100 - 50 - 30 - 15 = 5 more.\nThe final answer is 5.\n\nContext: Julie is reading a 120-page book. Yesterday, Julie was able to read 12 pages and today, she read twice as many pages as yesterday. Julie' s mother makes $18.00 an hour. \nQuestion: How many pages are left to be read?\nAnswer:\nJulie read 12 x 2 = <<12*2=24>>24 pages today.\nSo she was able to read a total of 12 + 24 = 36 pages since yesterday.\nThere are 120 - 36 = 84 pages left to be read.\nSince she wants to read half of the remaining pages tomorrow, then she should read 84/2 = 42 pages.\nThe final answer is 42.\n\nContext: James writes a 2-page letter to 4 different friends, lived in America, twice a week.  James writes a 3-page letter to 2 different friends, lived in Japan,  twice a week.  \nQuestion: How many pages does James write each friend lived in Japan at one time?\nAnswer:\nHe writes each friend 3*2=6 pages a week.\nSo he writes 6*2=12 pages every week.\nThat means he writes 12*52=624 pages a year.\nThe final answer is 624.\n"
        
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    os.makedirs(Path(args.output_file).parent, exist_ok=True)
    
    with open(args.output_file, "w") as f, open(args.output_json_file, "w") as jf:
        for index in tqdm(range(len(inputs))):
            #response = str(palm.generate_text(prompt=prompt+inputs[index]).result)
            #response = send(prompt=prompt+inputs[index]+"\n".join(outputs[index][:args.depth]))
            response = send(prompt=prompt+inputs[index])

            
            json_data = {
                "input": inputs[index],
                "pred_output": response,
            }
            jf.write(json.dumps((json_data)))
            jf.write("\n")
            f.write("Context:\n")
            f.write(inputs[index]+"\n")
            f.write("Pred Reasoning Steps:\n")
            f.write(response+"\n")
            f.write("------------------\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input_file', default="test1,valid2")
    parser.add_argument('--output_file', default="save/test")
    parser.add_argument('--output_json_file', default="save/test")
    parser.add_argument('--prompt_type', default="flat")
    args = parser.parse_args()
    main(args)
