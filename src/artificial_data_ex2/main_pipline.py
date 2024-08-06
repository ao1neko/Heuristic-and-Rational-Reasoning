import argparse
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

import transformers
import torch
import json
import re
from pathlib import Path
from tqdm import tqdm

from src.artificial_data_ex2.utils import read_jsonl_file


def main(args):
    inputs, outputs, answers = read_jsonl_file(args.input_file)
    inputs = [x + "Answer:\n" for x in inputs]
    #inputs = inputs[:50]

    if args.prompt_type == "flat":
        prompt="Answer the context question according to the following example.\n\nContext: Walter has -22 apples. Ursula has 3 more apples than Walter. Victor has 3 more apples than Ursula. Quentin has 2 more apples than Ursula. Nancy has 3 more apples than Walter. Zoe has 3 more apples than Nancy. Heidi has 3 more apples than Nancy. Carol's mother has 4 apples. Xavier has 3 more apples than Carol's mother. Peggy has 4 more apples than Xavier. Dave has 13 more apples than Xavier. Bob has 1 more apples than Carol's mother. Alice has 3 more apples than Bob. Sybil has 56 more apples than Bob.\nQuestion: How many apples does Dave have?\nAnswer:\nCarol's mother has 4 apples, and Xavier has 3 more apples than Carol's mother. So, Xavier has 4+3=7 apples.\nXavier has 7 apples, and Dave has 13 more apples than Xavier. So, Dave has 7+13=20 apples. \nThe final answer is 20.\n\nContext: Alice has 92 more bananas than Mallory. Victor has 10 less bananas than Walter. Xavier has 59 more bananas than Sybil. Yvonne has 79 more bananas than Sybil. Judy has 23 more bananas than Alice. Dave has 60 more bananas than Victor. Quentin has 35 less bananas than Peggy. Heidi has 95 more bananas than Victor. Ursula doesn't have 32 more bananas than Peggy. Larry has 17 less bananas than Alice. Zoe has 58 less bananas than Yvonne. Ivan has 43 less bananas than Yvonne. Walter has 43 less bananas than Mallory. Nancy has 34 bananas. Grace has 41 more bananas than Xavier. Mallory has 55 less bananas than Nancy. Sybil has 3 less bananas than Nancy. Peggy has 50 more bananas than Walter. Trent has 33 less bananas than Xavier.\nQuestion: How many bananas does Quentin have?\nAnswer:\nNancy has 34 bananas, and Mallory has 55 less bananas than Nancy. So, Mallory has 34-55=-21 bananas.\nMallory has -21 bananas, and Walter has 43 less bananas than Mallory. So, Walter has -21-43=-64 bananas.\nWalter has -64 bananas, and Peggy has 50 more bananas than Walter. So, Peggy has -64+50=-14 bananas.\nPeggy has -14 bananas, and Quentin has 35 less bananas than Peggy. So, Quentin has -14-35=-49 bananas.\nThe final answer is -49.\n\nContext: Zoe has 10 more apples than Yvonne's son. Eve has 2 apples. Yvonne's son has 3 more apples than Eve. Quentin has 3 more apples than Yvonne. Yvonne has 3 less apples than Zoe. Alice has 3 more apples than Grace. Trent has 34 more apples than Zoe. Ivan has 3 apples.  Ursula has 3 more apples than Zoe. Grace has 3 apples. Xavier has 3 more apples than Ivan. \nQuestion: How many apples does Yvonne have?\nAnswer:\nEve has 2 apples, and Yvonne's son has 3 more apples than Eve. So, Yvonne's son has 2+3=5 apples. \nYvonne's son has 5 apples, and Zoe has 10 more apples than Yvonne's son. So, Zoe has 5+10=15 apples. \nZoe has 15 apples, and Yvonne has 3 less apples than Zoe. So, Yvonne has 15-3=12 apples. \nThe final answer is 12.\n\nContext: Kevin's friend has 33 less grapes than Rob. Ivan has 43 more grapes than Victor. Victor has 33 less grapes than Kevin's friend. Ursula has 75 less grapes than Zoe. Alice has 11 more grapes than Eve. Dave has 11 more grapes than Eve. Olivia has 29 more grapes than Kevin's friend. Mallory has 97 more grapes than Olivia. Judy has 78 more grapes than Olivia. Rob has 55 grapes. Frank has 70 less grapes than Heidi. Eve has 84 less grapes than Sybil. Xavier has 36 more grapes than Heidi. Sybil has 55 less grapes than Trent. Kevin has 43 less grapes than Zoe. Heidi has 61 less grapes than Trent. Zoe has 88 more grapes than Sybil. Trent has 40 more grapes than Rob. Walter has 38 more grapes than Victor.\nQuestion: How many grapes does Kevin have?\nAnswer:\nRob has 55 grapes, and Trent has 40 more grapes than Rob. So, Trent has 55+40=95 grapes.\nTrent has 95 grapes, and Sybil has 55 less grapes than Trent. So, Sybil has 95-55=40 grapes.\nSybil has 40 grapes, and Zoe has 88 more grapes than Sybil. So, Zoe has 40+88=128 grapes.\nZoe has 128 grapes, and Kevin has 43 less grapes than Zoe. So, Kevin has 128-43=85 grapes.\nThe final answer is 85.\n"
    elif args.prompt_type == "overlap":
        prompt="Answer the context question according to the following example.\n\nContext: Walter has -22 apples. Ursula has 3 more apples than Walter. Victor has 3 more apples than Ursula. Quentin has 2 more apples than Ursula. Nancy has 3 more apples than Walter. Zoe has 3 more apples than Nancy. Heidi has 3 more apples than Nancy. Dave's mother has 4 apples. Xavier has 3 more apples than Dave's mother. Peggy has 4 more apples than Xavier. Dave has 13 more apples than Xavier. Bob has 1 more apples than Carol's mother. Alice has 3 more apples than Bob. Sybil has 56 more apples than Bob.\nQuestion: How many apples does Dave have?\nAnswer:\nDave's mother has 4 apples, and Xavier has 3 more apples than Dave's mother. So, Xavier has 4+3=7 apples.\nXavier has 7 apples, and Dave has 13 more apples than Xavier. So, Dave has 7+13=20 apples. \nThe final answer is 10.\n\nContext: Larry has 6 more apples than Zoe. Ivan has 4 more apples than Nancy. Olivia has 3 apples. Zoe has 3 less apples than Sybil. Sybil has -1 apples. Nancy has 0 apples. Carol has 5 less apples than Olivia.\nQuestion: How many apples does Zoe have?\nAnswer:\nSybil has -1 apples, and Zoe has 3 less apples than Sybil. So, Zoe has -1-3=-4 apples.\nThe final answer is -4.\n\nContext: Zoe has 10 more apples than Yvonne's son. Eve has 2 apples. Yvonne's son has 3 more apples than Eve. Quentin has 3 more apples than Yvonne. Yvonne has 3 less apples than Zoe. Alice has 3 more apples than Grace. Trent has 34 more apples than Zoe. Ivan has 3 apples.  Ursula has 3 more apples than Zoe. Grace has 3 apples. Xavier has 3 more apples than Ivan. \nQuestion: How many apples does Yvonne have?\nAnswer:\nEve has 2 apples, and Yvonne's son has 3 more apples than Eve. So, Yvonne's son has 2+3=5 apples. \nYvonne's son has 5 apples, and Zoe has 10 more apples than Yvonne's son. So, Zoe has 5+10=15 apples. \nZoe has 15 apples, and Yvonne has 3 less apples than Zoe. So, Yvonne has 15-3=12 apples. \nThe final answer is 12.\n\nContext: Victor has 11 more apples than Kevin's friend. Judy has 3 less apples than Peggy. Rob has -2 more apples than Eve. Peggy has -5 apples. Walter has 3 more apples than Peggy. Eve has 3 apples. Kevin's friend has 3 more apples than Eve. Kevin has 12 more apples than Victor.\nQuestion: How many apples does Kevin have?\nAnswer:\nEve has 3 apples, and Kevin's friend has 3 more apples than Eve. So, Kevin's friend has 3+3=6 apples. \nKevin's friend has 6 apples, and Victor has 11 more apples than Kevin's friend. So, Victor has 6+11=17 apples. \nVictor has 17 apples, and Kevin has 12 more apples than Victor. So, Kevin has 17+12=29 apples.\nThe final answer is 29.\n"
    elif args.prompt_type == "negative":
        prompt="Answer the context question according to the following example.\n\nContext: Walter has -22 apples. Ursula has 3 more apples than Walter. Victor has 3 more apples than Ursula. Quentin has 2 more apples than Ursula. Nancy has 3 more apples than Walter. Zoe has 3 more apples than Nancy. Heidi has 3 more apples than Nancy. Carol's mother has 4 apples. Xavier has 3 less apples than Carol's mother. Peggy has 4 more apples than Xavier. Dave has 13 more apples than Xavier. Bob has 1 more apples than Carol's mother. Alice has 3 more apples than Bob. Sybil has 56 more apples than Bob.\nQuestion: How many apples does Dave have?\nAnswer:\nCarol's mother has 4 apples, and Xavier has 3 less apples than Carol's mother. So, Xavier has 4-3=1 apples.\nXavier has 1 apples, and Dave has 13 more apples than Xavier. So, Dave has 1+13=14 apples. \nThe final answer is 14.\n\nContext: Larry has 6 more apples than Zoe. Ivan has 4 more apples than Nancy. Olivia has 3 apples. Zoe has 3 less apples than Sybil. Sybil has -1 apples. Nancy has 0 apples. Carol has 5 more apples than Olivia.\nQuestion: How many apples does Zoe have?\nAnswer:\nSybil has -1 apples, and Zoe has 3 less apples than Sybil. So, Zoe has -1-3=-4 apples.\nThe final answer is -4.\n\nContext: Zoe has 10 more apples than Yvonne's son. Eve has 2 apples. Yvonne's son has 3 less apples than Eve. Quentin has 3 more apples than Yvonne. Yvonne has 3 less apples than Zoe. Alice has 3 more apples than Grace. Trent has 34 more apples than Zoe. Ivan has 3 apples.  Ursula has 3 more apples than Zoe. Grace has 3 apples. Xavier has 3 more apples than Ivan. \nQuestion: How many apples does Yvonne have?\nAnswer:\nEve has 2 apples, and Yvonne's son has 3 less apples than Eve. So, Yvonne's son has 2-3=-1 apples. \nYvonne's son has -1 apples, and Zoe has 10 more apples than Yvonne's son. So, Zoe has -1+10=9 apples. \nZoe has 9 apples, and Yvonne has 3 less apples than Zoe. So, Yvonne has 9-3=6 apples. \nThe final answer is 6.\n\nContext: Victor has 11 more apples than Mallory. Judy's father has 3 more apples than Peggy's father. Rob has -2 more apples than Eve. Peggy's father  has -5 apples. Walter has 3 more apples than Peggy's father. Eve has 3 apples. Mallory has 3 less apples than Eve. Kevin has 12 more apples than Victor.\nQuestion: How many apples does Kevin have?\nAnswer:\nEve has 3 apples, and Mallory has 3 less apples than Eve. So, Mallory has 3-3=0 apples. \nMallory has 0 apples, and Victor has 11 more apples than Mallory. So, Victor has 0+11=11 apples. \nVictor has 17 apples, and Kevin has 12 more apples than Victor. So, Kevin has 17+12=29 apples.\nThe final answer is 29.\n"
    elif args.prompt_type == "position":
        prompt="Answer the context question according to the following example.\n\nContext: Carol's mother has 4 apples. Xavier has 3 more apples than Carol's mother. Dave has 13 more apples than Xavier. Walter has -22 apples. Ursula has 3 more apples than Walter. Victor has 3 more apples than Ursula. Quentin has 2 more apples than Ursula. Nancy has 3 more apples than Walter. Zoe has 3 more apples than Nancy. Heidi has 3 more apples than Nancy. Peggy has 4 more apples than Xavier. Bob has 1 more apples than Carol's mother. Alice has 3 more apples than Bob. Sybil has 56 more apples than Bob. \nQuestion: How many apples does Dave have?\nAnswer:\nCarol's mother has 4 apples, and Xavier has 3 more apples than Carol's mother. So, Xavier has 4+3=7 apples.\nXavier has 7 apples, and Dave has 13 more apples than Xavier. So, Dave has 7+13=20 apples. \nThe final answer is 10.\n\nContext: Sybil has -1 apples. Zoe has 3 less apples than Sybil. Larry has 6 more apples than Zoe. Ivan has 4 more apples than Nancy.  Nancy has 0 apples. Carol has 5 less apples than Olivia. Olivia has 3 apples. \nQuestion: How many apples does Zoe have?\nAnswer:\nSybil has -1 apples, and Zoe has 3 less apples than Sybil. So, Zoe has -1-3=-4 apples.\nThe final answer is -4.\n\nContext: Eve has 2 apples. Yvonne's son has 3 more apples than Eve. Zoe has 10 more apples than Yvonne's son. Yvonne has 3 less apples than Zoe. Alice has 3 more apples than Grace. Quentin has 3 more apples than Yvonne. Trent has 34 more apples than Zoe. Ivan has 3 apples.  Ursula has 3 more apples than Zoe. Grace has 3 apples. Xavier has 3 more apples than Ivan. \nQuestion: How many apples does Yvonne have?\nAnswer:\nEve has 2 apples, and Yvonne's son has 3 more apples than Eve. So, Yvonne's son has 2+3=5 apples. \nYvonne's son has 5 apples, and Zoe has 10 more apples than Yvonne's son. So, Zoe has 5+10=15 apples. \nZoe has 15 apples, and Yvonne has 3 less apples than Zoe. So, Yvonne has 15-3=12 apples. \nThe final answer is 12.\n\nContext: Eve has 3 apples. Mallory has 3 more apples than Eve. Victor has 11 more apples than Mallory. Kevin has 12 more apples than Victor. Judy's father has 3 less apples than Peggy's father. Peggy's father has -5 apples. Walter has 3 more apples than Peggy's father. Rob has -2 more apples than Eve. \nQuestion: How many apples does Kevin have?\nAnswer:\nEve has 3 apples, and Mallory has 3 more apples than Eve. So, Mallory has 3+3=6 apples. \nMallory has 6 apples, and Victor has 11 more apples than Mallory. So, Victor has 6+11=17 apples. \nVictor has 17 apples, and Kevin has 12 more apples than Victor. So, Kevin has 17+12=29 apples.\nThe final answer is 29.\n"
    else:
        exit("Not implemented yet")

    """
    access_token = os.environ.get("HF_ACCESS_TOKEN")
    tokenizer = AutoTokenizer.from_pretrained(
        args.model,
        token=access_token,
        )
    print(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.float16,
        device_map="auto",
        token=access_token,
    )
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto",
        tokenizer=tokenizer,
        #model_kwargs={"load_in_8bit": True}
    )
    """
    tokenizer = AutoTokenizer.from_pretrained(
        args.model,
        )
    print(args.model)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto",
        tokenizer=tokenizer,
        #model_kwargs={"load_in_8bit": True}
    )

    
    os.makedirs(Path(args.output_file).parent, exist_ok=True)
    with open(Path(args.output_file), "w") as f, open(Path(args.output_json_file), "w") as jf:
        for index in tqdm(range(len(inputs))):
            response = pipeline(
                            prompt + inputs[index] +"\n".join(outputs[index][:args.depth]),
                            do_sample=False,
                            num_return_sequences=1,
                            max_new_tokens=60,
                            temperature=0.0,
                            pad_token_id=tokenizer.eos_token_id,
                            return_full_text=False)
            response = response[0]["generated_text"]
            
            json_data = {
                "input": inputs[index],
                "output": outputs[index],
                "pred_output": response,
            }
            jf.write(json.dumps((json_data)))
            jf.write("\n")
            f.write("Context:\n")
            f.write(inputs[index]+"\n")
            f.write("Correct Reasoning Steps:\n")
            f.write(str(outputs[index])+"\n")
            f.write("Answer:\n")
            f.write(str(answers[index])+"\n")
            f.write("Pred Reasoning Steps:\n")
            f.write(response+"\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input_file', default="test1,valid2")
    parser.add_argument('--output_file', default="save/test")
    parser.add_argument('--output_json_file', default="save/test")
    parser.add_argument('--prompt_type', default="flat")
    parser.add_argument('--model', default="text-davinci-003")
    parser.add_argument('--depth', default=0, type=int)
    args = parser.parse_args()
    main(args)
