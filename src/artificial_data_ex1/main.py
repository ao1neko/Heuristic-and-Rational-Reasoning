import argparse
import os

import json
from src.classes.executor_class import GPT
from src.artificial_data_ex1.utils import read_jsonl_file
from pathlib import Path
from tqdm import tqdm

def main(args):
    inputs, outputs, _,sentence_ps,number_ps = read_jsonl_file(args.input_file)
    #inputs = inputs[:30]

    if args.prompt_type == "flat":
        prompt=[
    {
      "role": "system",
      "content": [
        {
          "text": "Answer the context question according to the following example.\n",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Walter has -22 apples. Ursula has 3 more apples than Walter. Victor has 3 more apples than Ursula. Quentin has 2 more apples than Ursula. Nancy has 3 more apples than Walter. Zoe has 3 more apples than Nancy. Heidi has 3 more apples than Nancy. Carol's mother has 4 apples. Xavier has 3 more apples than Carol's mother. Peggy has 4 more apples than Xavier. Dave has 13 more apples than Xavier. Bob has 1 more apples than Carol's mother. Alice has 3 more apples than Bob. Sybil has 56 more apples than Bob.\nQuestion: How many apples does Dave have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nCarol's mother has 4 apples, and Xavier has 3 more apples than Carol's mother. So, Xavier has 4+3=7 apples.\nXavier has 7 apples, and Dave has 13 more apples than Xavier. So, Dave has 7+13=20 apples. \nThe final answer is 20.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Alice has 92 more bananas than Mallory. Victor has 10 less bananas than Walter. Xavier has 59 more bananas than Sybil. Yvonne has 79 more bananas than Sybil. Judy has 23 more bananas than Alice. Dave has 60 more bananas than Victor. Quentin has 35 less bananas than Peggy. Heidi has 95 more bananas than Victor. Ursula doesn't have 32 more bananas than Peggy. Larry has 17 less bananas than Alice. Zoe has 58 less bananas than Yvonne. Ivan has 43 less bananas than Yvonne. Walter has 43 less bananas than Mallory. Nancy has 34 bananas. Grace has 41 more bananas than Xavier. Mallory has 55 less bananas than Nancy. Sybil has 3 less bananas than Nancy. Peggy has 50 more bananas than Walter. Trent has 33 less bananas than Xavier.\nQuestion: How many bananas does Quentin have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nNancy has 34 bananas, and Mallory has 55 less bananas than Nancy. So, Mallory has 34-55=-21 bananas.\nMallory has -21 bananas, and Walter has 43 less bananas than Mallory. So, Walter has -21-43=-64 bananas.\nWalter has -64 bananas, and Peggy has 50 more bananas than Walter. So, Peggy has -64+50=-14 bananas.\nPeggy has -14 bananas, and Quentin has 35 less bananas than Peggy. So, Quentin has -14-35=-49 bananas.\nThe final answer is -49.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Zoe has 10 more apples than Yvonne's son. Eve has 2 apples. Yvonne's son has 3 more apples than Eve. Quentin has 3 more apples than Yvonne. Yvonne has 3 less apples than Zoe. Alice has 3 more apples than Grace. Trent has 34 more apples than Zoe. Ivan has 3 apples.  Ursula has 3 more apples than Zoe. Grace has 3 apples. Xavier doesn't have 3 more apples than Ivan. \nQuestion: How many apples does Yvonne have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nEve has 2 apples, and Yvonne's son has 3 more apples than Eve. So, Yvonne's son has 2+3=5 apples. \nYvonne's son has 5 apples, and Zoe has 10 more apples than Yvonne's son. So, Zoe has 5+10=15 apples. \nZoe has 15 apples, and Yvonne has 3 less apples than Zoe. So, Yvonne has 15-3=12 apples. \nThe final answer is 12.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Kevin's friend has 33 less grapes than Rob. Ivan has 43 more grapes than Victor. Victor has 33 less grapes than Kevin's friend. Ursula has 75 less grapes than Zoe. Alice has 11 more grapes than Eve. Dave has 11 more grapes than Eve. Olivia has 29 more grapes than Kevin's friend. Mallory has 97 more grapes than Olivia. Judy has 78 more grapes than Olivia. Rob has 55 grapes. Frank has 70 less grapes than Heidi. Eve has 84 less grapes than Sybil. Xavier has 36 more grapes than Heidi. Sybil has 55 less grapes than Trent. Kevin has 43 less grapes than Zoe. Heidi has 61 less grapes than Trent. Zoe has 88 more grapes than Sybil. Trent has 40 more grapes than Rob. Walter has 38 more grapes than Victor.\nQuestion: How many grapes does Kevin have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nRob has 55 grapes, and Trent has 40 more grapes than Rob. So, Trent has 55+40=95 grapes.\nTrent has 95 grapes, and Sybil has 55 less grapes than Trent. So, Sybil has 95-55=40 grapes.\nSybil has 40 grapes, and Zoe has 88 more grapes than Sybil. So, Zoe has 40+88=128 grapes.\nZoe has 128 grapes, and Kevin has 43 less grapes than Zoe. So, Kevin has 128-43=85 grapes.\nThe final answer is 128.",
          "type": "text"
        }
      ]
    }
  ]
    elif args.prompt_type == "overlap":
      prompt = [
    {
      "role": "system",
      "content": [
        {
          "text": "Answer the context question according to the following example.\n",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Walter has -22 apples. Ursula has 3 more apples than Walter. Victor has 3 more apples than Ursula. Quentin has 2 more apples than Ursula. Nancy has 3 more apples than Walter. Zoe has 3 more apples than Nancy. Heidi has 3 more apples than Nancy. Dave's mother has 4 apples. Dave's father has 3 more apples than Dave's mother. Peggy has 4 more apples than Dave's father. Dave has 13 more apples than Dave's father. Bob has 1 more apples than Carol's mother. Alice has 3 more apples than Bob. Sybil has 56 more apples than Bob.\nQuestion: How many apples does Dave have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nDave's mother has 4 apples, and Dave's father has 3 more apples than Dave's mother. So, Dave's father has 4+3=7 apples.\nDave's father has 7 apples, and Dave has 13 more apples than Dave's father. So, Dave has 7+13=20 apples. \nThe final answer is 10.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Alice has 92 more bananas than Quentin's mother. Victor has 10 less bananas than Walter. Xavier has 59 more bananas than Sybil. Yvonne has 79 more bananas than Sybil. Judy has 23 more bananas than Alice. Dave has 60 more bananas than Victor. Quentin has 35 less bananas than Quentin's father. Heidi has 95 more bananas than Victor. Ursula doesn't have 32 more bananas than Quentin's father. Larry has 17 less bananas than Alice. Zoe has 58 less bananas than Yvonne. Ivan has 43 less bananas than Yvonne. Walter has 43 less bananas than Quentin's mother. Nancy has 34 bananas. Grace has 41 more bananas than Xavier. Quentin's mother has 55 less bananas than Nancy. Sybil has 3 less bananas than Nancy. Quentin's father has 50 more bananas than Walter. Trent has 33 less bananas than Xavier.\nQuestion: How many bananas does Quentin have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nNancy has 34 bananas, and Quentin's mother has 55 less bananas than Nancy. So, Quentin's mother has 34-55=-21 bananas.\nQuentin's mother has -21 bananas, and Walter has 43 less bananas than Quentin's mother. So, Walter has -21-43=-64 bananas.\nWalter has -64 bananas, and Quentin's father has 50 more bananas than Walter. So, Quentin's father has -64+50=-14 bananas.\nQuentin's father has -14 bananas, and Quentin has 35 less bananas than Quentin's father. So, Quentin has -14-35=-49 bananas.\nThe final answer is -49.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Yvonne's father has 10 more apples than Yvonne's son. Eve has 2 apples. Yvonne's son has 3 more apples than Eve. Quentin has 3 more apples than Yvonne. Yvonne has 3 less apples than Yvonne's father. Alice has 3 more apples than Grace. Trent has 34 more apples than Yvonne's father. Ivan has 3 apples.  Ursula has 3 more apples than Yvonne's father. Grace has 3 apples. Xavier has 3 more apples than Ivan. \nQuestion: How many apples does Yvonne have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nEve has 2 apples, and Yvonne's son has 3 more apples than Eve. So, Yvonne's son has 2+3=5 apples. \nYvonne's son has 5 apples, and Yvonne's father has 10 more apples than Yvonne's son. So, Yvonne's father has 5+10=15 apples. \nYvonne's father has 15 apples, and Yvonne has 3 less apples than Yvonne's father. So, Yvonne has 15-3=12 apples. \nThe final answer is 12.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Kevin's friend has 33 less grapes than Rob. Ivan has 43 more grapes than Victor. Victor has 33 less grapes than Kevin's friend. Ursula has 75 less grapes than Zoe. Alice has 11 more grapes than Eve. Dave has 11 more grapes than Eve. Olivia has 29 more grapes than Kevin's friend. Mallory has 97 more grapes than Olivia. Judy has 78 more grapes than Olivia. Rob has 55 grapes. Frank has 70 less grapes than Heidi. Eve has 84 less grapes than Kevin's neighborhood. Xavier has 36 more grapes than Heidi. Kevin's neighborhood has 55 less grapes than Kevin's friend. Kevin has 43 less grapes than Kevin's mother. Heidi has 61 less grapes than Kevin's friend. Kevin's mother has 88 more grapes than Kevin's neighborhood. Kevin's friend has 40 more grapes than Rob. Walter has 38 more grapes than Victor.\nQuestion: How many grapes does Kevin have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nRob has 55 grapes, and Kevin's friend has 40 more grapes than Rob. So, Kevin's friend has 55+40=95 grapes.\nKevin's friend has 95 grapes, and Kevin's neighborhood has 55 less grapes than Kevin's friend. So, Kevin's neighborhood has 95-55=40 grapes.\nKevin's neighborhood has 40 grapes, and Kevin's mother has 88 more grapes than Kevin's neighborhood. So, Kevin's mother has 40+88=128 grapes.\nKevin's mother has 128 grapes, and Kevin has 43 less grapes than Kevin's mother. So, Kevin has 128-43=85 grapes.\nThe final answer is 128.",
          "type": "text"
        }
      ]
    }
  ]
    elif args.prompt_type == "negative":
        prompt = [
    {
      "role": "system",
      "content": [
        {
          "text": "Answer the context question according to the following example.\n",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Walter doesn't have -22 apples. Ursula has 3 more apples than Walter. Victor has 3 more apples than Ursula. Quentin has 2 more apples than Ursula. Nancy doesn't have 3 more apples than Walter. Zoe has 3 more apples than Nancy. Heidi doesn't have 3 more apples than Nancy. Carol's mother has 4 apples. Xavier has 3 more apples than Carol's mother. Peggy has 4 more apples than Xavier. Dave has 13 more apples than Xavier. Bob doesn't have 1 more apples than Carol's mother. Alice has 3 more apples than Bob. Sybil has 56 more apples than Bob.\nQuestion: How many apples does Dave have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nCarol's mother has 4 apples, and Xavier has 3 more apples than Carol's mother. So, Xavier has 4+3=7 apples.\nXavier has 7 apples, and Dave has 13 more apples than Xavier. So, Dave has 7+13=20 apples. \nThe final answer is 20.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Alice has 92 more bananas than Mallory. Victor has 10 less bananas than Walter. Xavier has 59 more bananas than Sybil. Yvonne doesn't have 79 more bananas than Sybil. Judy doesn't have 23 more bananas than Alice. Dave has 60 more bananas than Victor. Quentin has 35 less bananas than Peggy. Heidi has 95 more bananas than Victor. Ursula doesn't have 32 more bananas than Peggy. Larry doesn't have 17 less bananas than Alice. Zoe has 58 less bananas than Yvonne. Ivan has 43 less bananas than Yvonne. Walter has 43 less bananas than Mallory. Nancy has 34 bananas. Grace doesn't have 41 more bananas than Xavier. Mallory has 55 less bananas than Nancy. Sybil doesn't have 3 less bananas than Nancy. Peggy has 50 more bananas than Walter. Trent doesn't have 33 less bananas than Xavier.\nQuestion: How many bananas does Quentin have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nNancy has 34 bananas, and Mallory has 55 less bananas than Nancy. So, Mallory has 34-55=-21 bananas.\nMallory has -21 bananas, and Walter has 43 less bananas than Mallory. So, Walter has -21-43=-64 bananas.\nWalter has -64 bananas, and Peggy has 50 more bananas than Walter. So, Peggy has -64+50=-14 bananas.\nPeggy has -14 bananas, and Quentin has 35 less bananas than Peggy. So, Quentin has -14-35=-49 bananas.\nThe final answer is -49.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Zoe has 10 more apples than Yvonne's son. Eve has 2 apples. Yvonne's son has 3 more apples than Eve. Quentin has 3 more apples than Yvonne. Yvonne has 3 less apples than Zoe. Alice has 3 more apples than Grace. Trent has 34 more apples than Zoe. Ivan has 3 apples.  Ursula has 3 more apples than Zoe. Grace has 3 apples. Xavier doesn't have 3 more apples than Ivan. \nQuestion: How many apples does Yvonne have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nEve has 2 apples, and Yvonne's son has 3 more apples than Eve. So, Yvonne's son has 2+3=5 apples. \nYvonne's son has 5 apples, and Zoe has 10 more apples than Yvonne's son. So, Zoe has 5+10=15 apples. \nZoe has 15 apples, and Yvonne has 3 less apples than Zoe. So, Yvonne has 15-3=12 apples. \nThe final answer is 12.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Kevin's friend has 33 less grapes than Rob. Ivan doesn't have 43 more grapes than Victor. Victor doesn't have 33 less grapes than Kevin's friend. Ursula has 75 less grapes than Zoe. Alice has 11 more grapes than Eve. Dave has 11 more grapes than Eve. Olivia doesn't have 29 more grapes than Kevin's friend. Mallory has 97 more grapes than Olivia. Judy doesn't have 78 more grapes than Olivia. Rob has 55 grapes. Frank has 70 less grapes than Heidi. Eve has 84 less grapes than Sybil. Xavier doesn't 36 more grapes than Heidi. Sybil has 55 less grapes than Trent. Kevin has 43 less grapes than Zoe. Heidi has 61 less grapes than Trent. Zoe has 88 more grapes than Sybil. Trent has 40 more grapes than Rob. Walter has 38 more grapes than Victor.\nQuestion: How many grapes does Kevin have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nRob has 55 grapes, and Trent has 40 more grapes than Rob. So, Trent has 55+40=95 grapes.\nTrent has 95 grapes, and Sybil has 55 less grapes than Trent. So, Sybil has 95-55=40 grapes.\nSybil has 40 grapes, and Zoe has 88 more grapes than Sybil. So, Zoe has 40+88=128 grapes.\nZoe has 128 grapes, and Kevin has 43 less grapes than Zoe. So, Kevin has 128-43=85 grapes.\nThe final answer is 128.",
          "type": "text"
        }
      ]
    }
  ]
    elif args.prompt_type == "position":
        prompt =[
    {
      "role": "system",
      "content": [
        {
          "text": "Answer the context question according to the following example.\n",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Carol's mother has 4 apples. Xavier has 3 more apples than Carol's mother. Dave has 13 more apples than Xavier. Walter has -22 apples. Ursula has 3 more apples than Walter. Victor has 3 more apples than Ursula. Quentin has 2 more apples than Ursula. Nancy has 3 more apples than Walter. Zoe has 3 more apples than Nancy. Heidi has 3 more apples than Nancy. Peggy has 4 more apples than Xavier. Bob has 1 more apples than Carol's mother. Alice has 3 more apples than Bob. Sybil has 56 more apples than Bob. \nQuestion: How many apples does Dave have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nCarol's mother has 4 apples, and Xavier has 3 more apples than Carol's mother. So, Xavier has 4+3=7 apples.\nXavier has 7 apples, and Dave has 13 more apples than Xavier. So, Dave has 7+13=20 apples. \nThe final answer is 20.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Nancy has 34 bananas. Mallory has 55 less bananas than Nancy. Walter has 43 less bananas than Mallory. Peggy has 50 more bananas than Walter. Quentin has 35 less bananas than Peggy. Alice has 92 more bananas than Mallory. Victor has 10 less bananas than Walter. Xavier has 59 more bananas than Sybil. Yvonne has 79 more bananas than Sybil. Judy has 23 more bananas than Alice. Dave has 60 more bananas than Victor. Heidi has 95 more bananas than Victor. Ursula doesn't have 32 more bananas than Peggy. Larry has 17 less bananas than Alice. Zoe has 58 less bananas than Yvonne. Ivan has 43 less bananas than Yvonne. Grace has 41 more bananas than Xavier. Sybil has 3 less bananas than Nancy. Trent has 33 less bananas than Xavier.\nQuestion: How many bananas does Quentin have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nNancy has 34 bananas, and Mallory has 55 less bananas than Nancy. So, Mallory has 34-55=-21 bananas.\nMallory has -21 bananas, and Walter has 43 less bananas than Mallory. So, Walter has -21-43=-64 bananas.\nWalter has -64 bananas, and Peggy has 50 more bananas than Walter. So, Peggy has -64+50=-14 bananas.\nPeggy has -14 bananas, and Quentin has 35 less bananas than Peggy. So, Quentin has -14-35=-49 bananas.\nThe final answer is -49.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Eve has 2 apples. Yvonne's son has 3 more apples than Eve. Zoe has 10 more apples than Yvonne's son. Yvonne has 3 less apples than Zoe. Alice has 3 more apples than Grace. Quentin has 3 more apples than Yvonne. Trent has 34 more apples than Zoe. Ivan has 3 apples.  Ursula has 3 more apples than Zoe. Grace has 3 apples. Xavier has 3 more apples than Ivan. \nQuestion: How many apples does Yvonne have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nEve has 2 apples, and Yvonne's son has 3 more apples than Eve. So, Yvonne's son has 2+3=5 apples. \nYvonne's son has 5 apples, and Zoe has 10 more apples than Yvonne's son. So, Zoe has 5+10=15 apples. \nZoe has 15 apples, and Yvonne has 3 less apples than Zoe. So, Yvonne has 15-3=12 apples. \nThe final answer is 12.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Rob has 55 grapes. Trent has 40 more grapes than Rob. Sybil has 55 less grapes than Trent. Zoe has 88 more grapes than Sybil. Kevin has 43 less grapes than Zoe. Kevin's friend has 33 less grapes than Rob. Ivan has 43 more grapes than Victor. Victor has 33 less grapes than Kevin's friend. Ursula has 75 less grapes than Zoe. Alice has 11 more grapes than Eve. Dave has 11 more grapes than Eve. Olivia has 29 more grapes than Kevin's friend. Mallory has 97 more grapes than Olivia. Judy has 78 more grapes than Olivia. Frank has 70 less grapes than Heidi. Eve has 84 less grapes than Sybil. Xavier has 36 more grapes than Heidi. Heidi has 61 less grapes than Trent. Walter has 38 more grapes than Victor.\nQuestion: How many grapes does Kevin have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Answer:\nRob has 55 grapes, and Trent has 40 more grapes than Rob. So, Trent has 55+40=95 grapes.\nTrent has 95 grapes, and Sybil has 55 less grapes than Trent. So, Sybil has 95-55=40 grapes.\nSybil has 40 grapes, and Zoe has 88 more grapes than Sybil. So, Zoe has 40+88=128 grapes.\nZoe has 128 grapes, and Kevin has 43 less grapes than Zoe. So, Kevin has 128-43=85 grapes.\nThe final answer is 128.",
          "type": "text"
        }
      ]
    }
  ]
    elif args.prompt_type == "step_flat":
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
          "text": "Context: Walter has -22 apples. Ursula has 3 more apples than Walter. Victor has 3 more apples than Ursula. Quentin has 2 more apples than Ursula. Nancy has 3 more apples than Walter. Zoe has 3 more apples than Nancy. Heidi has 3 more apples than Nancy. Carol's mother has 4 apples. Xavier has 3 more apples than Carol's mother. Peggy has 4 more apples than Xavier. Dave has 13 more apples than Xavier. Bob has 1 more apples than Carol's mother. Alice has 3 more apples than Bob. Sybil has 56 more apples than Bob.\nQuestion: How many apples does Dave have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Carol's mother has 4 apples, and Xavier has 3 more apples than Carol's mother. So, Xavier has 4+3=7 apples.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Xavier has 7 apples, and Dave has 13 more apples than Xavier. So, Dave has 7+13=20 apples. ",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The final answer is 10.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Larry has 6 more apples than Zoe. Ivan has 4 more apples than Nancy. Olivia has 3 apples. Zoe has 3 less apples than Sybil. Sybil has -1 apples. Nancy has 0 apples. Carol has 5 less apples than Olivia.\nQuestion: How many apples does Zoe have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Sybil has -1 apples, and Zoe has 3 less apples than Sybil. So, Zoe has -1-3=-4 apples.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The final answer is -4.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Zoe has 10 more apples than Yvonne's son. Eve has 2 apples. Yvonne's son has 3 more apples than Eve. Quentin has 3 more apples than Yvonne. Yvonne has 3 less apples than Zoe. Alice has 3 more apples than Grace. Trent has 34 more apples than Zoe. Ivan has 3 apples.  Ursula has 3 more apples than Zoe. Grace has 3 apples. Xavier has 3 more apples than Ivan. \nQuestion: How many apples does Yvonne have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Eve has 2 apples, and Yvonne's son has 3 more apples than Eve. So, Yvonne's son has 2+3=5 apples. ",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Yvonne's son has 5 apples, and Zoe has 10 more apples than Yvonne's son. So, Zoe has 5+10=15 apples. ",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Zoe has 15 apples, and Yvonne has 3 less apples than Zoe. So, Yvonne has 15-3=12 apples. ",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The final answer is 12.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Victor has 11 more apples than Mallory. Judy's father has 3 less apples than Peggy's father. Rob has -2 more apples than Eve. Peggy's father  has -5 apples. Walter has 3 more apples than Peggy's father. Eve has 3 apples. Mallory has 3 more apples than Eve. Kevin has 12 more apples than Victor.\nHow many apples does Kevin have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Eve has 3 apples, and Mallory has 3 more apples than Eve. So, Mallory has 3+3=6 apples. ",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Mallory has 6 apples, and Victor has 11 more apples than Mallory. So, Victor has 6+11=17 apples. ",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Victor has 17 apples, and Kevin has 12 more apples than Victor. So, Kevin has 17+12=29 apples.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The final answer is 29.",
          "type": "text"
        }
      ]
    }
  ]
    elif args.prompt_type == "step_logic":
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
          "text": "Context: Walter has -22 apples. Ursula has 3 more apples than Walter. Victor has 3 more apples than Ursula. Quentin has 2 more apples than Ursula. Nancy has 3 more apples than Walter. Zoe has 3 more apples than Nancy. Heidi has 3 more apples than Nancy. Carol's mother has 4 apples. Xavier has 3 more apples than Carol's mother. Peggy has 4 more apples than Xavier. Dave has 13 more apples than Xavier. Bob has 1 more apples than Carol's mother. Alice has 3 more apples than Bob. Sybil has 56 more apples than Bob.\nQuestion: How many apples does Dave have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Walter has -22 apples, and Ursula has 3 more apples than Walter. So, Walter has -22+3=-19 apples.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Carol's mother has 4 apples, and Xavier has 3 more apples than Carol's mother. So, Xavier has 4+3=7 apples.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Xavier has 7 apples, and Dave has 13 more apples than Xavier. So, Dave has 7+13=20 apples. ",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The final answer is 10.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Larry has 6 more apples than Zoe. Ivan has 4 more apples than Nancy. Olivia has 3 apples. Zoe has 3 less apples than Sybil. Sybil has -1 apples. Nancy has 0 apples. Carol has 5 less apples than Olivia.\nQuestion: How many apples does Zoe have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Olivia has 3 apples, and Carol has 5 less apples than Olivia. So, Carol has 3-5=2 apples.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Sybil has -1 apples, and Zoe has 3 less apples than Sybil. So, Zoe has -1-3=-4 apples.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The final answer is -4.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Zoe has 10 more apples than Yvonne's son. Eve has 2 apples. Yvonne's son has 3 more apples than Eve. Quentin has 3 more apples than Yvonne. Yvonne has 3 less apples than Zoe. Alice has 3 more apples than Grace. Trent has 34 more apples than Zoe. Ivan has 3 apples.  Ursula has 3 more apples than Zoe. Grace has 3 apples. Xavier has 3 more apples than Ivan. \nQuestion: How many apples does Yvonne have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Eve has 2 apples, and Yvonne's son has 3 more apples than Eve. So, Yvonne's son has 2+3=5 apples. ",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Yvonne's son has 5 apples, and Zoe has 10 more apples than Yvonne's son. So, Zoe has 5+10=15 apples. ",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Zoe has 15 apples, and Yvonne has 3 less apples than Zoe. So, Yvonne has 15-3=12 apples. ",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The final answer is 12.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Victor has 11 more apples than Mallory. Judy's father has 3 less apples than Peggy's father. Rob has -2 more apples than Eve. Peggy's father  has -5 apples. Walter has 3 more apples than Peggy's father. Eve has 3 apples. Mallory has 3 more apples than Eve. Kevin has 12 more apples than Victor.\nQuestion: How many apples does Kevin have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Peggy's father  has -5 apples, and Judy's father has 3 less apples than Peggy's father. So, Judy's father has-5-3=-8 apples.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Eve has 3 apples, and Mallory has 3 more apples than Eve. So, Mallory has 3+3=6 apples. ",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Mallory has 6 apples, and Victor has 11 more apples than Mallory. So, Victor has 6+11=17 apples. ",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Victor has 17 apples, and Kevin has 12 more apples than Victor. So, Kevin has 17+12=29 apples.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The final answer is 29.",
          "type": "text"
        }
      ]
    }
  ]
    elif args.prompt_type == "no_reasoning":
        prompt = [
            {
            "role": "system",
            "content": "Answer the context question according to the following example. \n\n\n"
            },
            {
            "role": "user",
            "content": "Context: Judy is not youthful. If Judy is cute, then Walter is small. If Sybil is not rich, then Walter is smart. If Alice is not kind, then Dave is beautiful. If Grace is smart, then Dave is not witty. Xavier is clever. Sybil is not rich. If Trent is pretty, then Ursula is rich. If Olivia is rich, then Ivan is not pretty. If Ursula is rich, then Dave is not beautiful. If Ursula is kind, then Ivan is not small. If Dave is pretty, then Judy is cute. If Xavier is clever, then Grace is smart. If Ivan is not pretty, then Dave is not beautiful. If Dave is not witty, then Trent is ill. If Dave is not funny, then Ursula is not tall. If Judy is not youthful, then Grace is funny. If Ivan is not small, then Trent is not kind. If Walter is smart, then Olivia is rich. If Grace is funny, then Ursula is kind. If Trent is ill, then Yvonne is smart. If Ursula is not tall, then Trent is pretty. If Walter is small, then Alice is not kind.\nQuestion: Dave is beautiful?"
            },
            {
            "role": "assistant",
            "content": "The final answer is False."
            },
            {
            "role": "user",
            "content": "Context: Frank is kind. Yvonne is not rich. Nancy is witty.\nQuestion: Yvonne is rich?"
            },
            {
            "role": "assistant",
            "content": "Yvonne is not rich. The final answer is False."
            },
            {
            "role": "user",
            "content": "Context: If Ursula is witty, then Grace is not wonderful. If Ivan is not beautiful, then Quentin is not clever. If Grace is not beautiful, then Trent is not smart. If Grace is not wonderful, then Ivan is not small. If Trent is not smart, then Walter is not beautiful. If Peggy is honest, then Heidi is hungry. If Quentin is not clever, then Sybil is not rich. Ivan is not beautiful. If Frank is cute, then Heidi is rich. If Heidi is hungry, then Ivan is small. Grace is not beautiful. If Heidi is rich, then Ivan is small. Peggy is honest.\nQuestion: Ivan is small?"
            },
            {
            "role": "assistant",
            "content": "The final answer is True."
            },
            {
            "role": "user",
            "content": "Context: If Larry is smart, then Zoe is not pretty. If Larry is not youthful, then Zoe is not pretty. If Nancy is smart, then Ivan is not rich. Olivia is not wonderful. If Sybil is not ill, then Zoe is not pretty. Sybil is not ill. Nancy is smart. If Olivia is not wonderful, then Carol is not clever.\nQuestion: Zoe is not pretty?\n"
            },
            {
            "role": "assistant",
            "content": "The final answer is True."
            },
            {
            "role": "user",
            "content": "Context: Ivan is beautiful. If Eve is not small, then Dave is wonderful. If Zoe is not wonderful, then Yvonne is not ill. If Zoe is hungry, then Zoe is not good. If Ursula is not youthful, then Yvonne is not ill. If Quentin is not kind, then Yvonne is not handsome. If Victor is honest, then Heidi is handsome. If Ivan is beautiful, then Zoe is tall. If Yvonne is not handsome, then Ursula is not youthful. Grace is not wonderful. If Sybil is not cute, then Victor is honest. Eve is not small. If Grace is not wonderful, then Zoe is hungry. If Judy is youthful, then Trent is small. If Zoe is tall, then Judy is youthful. If Heidi is handsome, then Yvonne is ill. If Zoe is not good, then Ursula is not pretty. If Dave is wonderful, then Zoe is not wonderful.\nQuestion: Yvonne is ill?"
            },
            {
            "role": "assistant",
            "content": "The final answer is False."
            }
        ]  
    else:
        exit("Not implemented yet")
    
    module = GPT(prompt=prompt, model=args.model)
    
    os.makedirs(Path(args.output_file).parent, exist_ok=True)
    with open(args.output_file, "w") as f, open(args.output_json_file, "w") as jf:
        for index in tqdm(range(0, len(inputs))):
            response = module.send(context=inputs[index])

            json_data = {
                "input": inputs[index],
                "output": outputs[index],
                "pred_output": response,
                "sentence_p": sentence_ps[index],
                "number_ps": number_ps[index],
            }
            jf.write(json.dumps((json_data)))
            jf.write("\n")
            f.write("Context:\n")
            f.write(inputs[index]+"\n")
            f.write("Correct Reasoning Steps:\n")
            f.write(str(outputs[index])+"\n")
            f.write("Pred Reasoning Steps:\n")
            f.write(response+"\n")
            f.write("sentence_p:\n")
            f.write(sentence_ps[index]+"\n")
            f.write("------------------\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input_file', default="test1,valid2")
    parser.add_argument('--output_file', default="save/test")
    parser.add_argument('--output_json_file', default="save/test")
    parser.add_argument('--prompt_type', default="flat")
    parser.add_argument('--model', default="text-davinci-003")
    args = parser.parse_args()
    main(args)
