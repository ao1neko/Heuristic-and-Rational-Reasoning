import argparse
import os

import json
from src.classes.executor_class import GPT
from src.artificial_data_ex2.utils import read_jsonl_file
from pathlib import Path
from tqdm import tqdm


def main(args):
    inputs, outputs, _ = read_jsonl_file(args.input_file)
    #inputs = inputs[:50]

    if args.prompt_type == "flat":
        prompt=[
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
          "text": "The final answer is 20.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Alice has 92 more bananas than Mallory. Victor has 10 fewer bananas than Walter. Xavier has 59 more bananas than Sybil. Yvonne has 79 more bananas than Sybil. Judy has 23 more bananas than Alice. Dave has 60 more bananas than Victor. Quentin has 35 fewer bananas than Peggy. Heidi has 95 more bananas than Victor. Ursula doesn't have 32 more bananas than Peggy. Larry has 17 fewer bananas than Alice. Zoe has 58 fewer bananas than Yvonne. Ivan has 43 fewer bananas than Yvonne. Walter has 43 fewer bananas than Mallory. Nancy has 34 bananas. Grace has 41 more bananas than Xavier. Mallory has 55 fewer bananas than Nancy. Sybil has 3 fewer bananas than Nancy. Peggy has 50 more bananas than Walter. Trent has 33 fewer bananas than Xavier.\nQuestion: How many bananas does Quentin have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Nancy has 34 bananas, and Mallory has 55 fewer bananas than Nancy. So, Mallory has 34-55=-21 bananas.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Mallory has -21 bananas, and Walter has 43 fewer bananas than Mallory. So, Walter has -21-43=-64 bananas.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Walter has -64 bananas, and Peggy has 50 more bananas than Walter. So, Peggy has -64+50=-14 bananas.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Peggy has -14 bananas, and Quentin has 35 fewer bananas than Peggy. So, Quentin has -14-35=-49 bananas.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "The final answer is -49."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Zoe has 10 more apples than Yvonne's son. Eve has 2 apples. Yvonne's son has 3 more apples than Eve. Quentin has 3 more apples than Yvonne. Yvonne has 3 fewer apples than Zoe. Alice has 3 more apples than Grace. Trent has 34 more apples than Zoe. Ivan has 3 apples.  Ursula has 3 more apples than Zoe. Grace has 3 apples. Xavier doesn't have 3 more apples than Ivan. \nQuestion: How many apples does Yvonne have?",
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
          "text": "Zoe has 15 apples, and Yvonne has 3 fewer apples than Zoe. So, Yvonne has 15-3=12 apples. ",
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
          "text": "Context: Kevin's friend has 33 fewer grapes than Rob. Ivan has 43 more grapes than Victor. Victor has 33 fewer grapes than Kevin's friend. Ursula has 75 fewer grapes than Zoe. Alice has 11 more grapes than Eve. Dave has 11 more grapes than Eve. Olivia has 29 more grapes than Kevin's friend. Mallory has 97 more grapes than Olivia. Judy has 78 more grapes than Olivia. Rob has 55 grapes. Frank has 70 fewer grapes than Heidi. Eve has 84 fewer grapes than Sybil. Xavier has 36 more grapes than Heidi. Sybil has 55 fewer grapes than Trent. Kevin has 43 fewer grapes than Zoe. Heidi has 61 fewer grapes than Trent. Zoe has 88 more grapes than Sybil. Trent has 40 more grapes than Rob. Walter has 38 more grapes than Victor.\nQuestion: How many grapes does Kevin have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Rob has 55 grapes, and Trent has 40 more grapes than Rob. So, Trent has 55+40=95 grapes.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Trent has 95 grapes, and Sybil has 55 fewer grapes than Trent. So, Sybil has 95-55=40 grapes.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Sybil has 40 grapes, and Zoe has 88 more grapes than Sybil. So, Zoe has 40+88=128 grapes.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "Zoe has 128 grapes, and Kevin has 43 fewer grapes than Zoe. So, Kevin has 128-43=85 grapes.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "The final answer is 85."
        }
      ]
    }
  ]
    elif args.prompt_type == "flat_distract":
        prompt=[
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
          "text": "Context: Kristopher has 36 fewer grapes than Olive. Mallory has 17 more grapes than Debbi. Yvonne has 33 more grapes than Gina. Kara has 5 more grapes than Kristopher. Frank has 59 fewer grapes than Olive. Brande has 29 more grapes than Debbi. Ben has 73 fewer grapes than Olive. Sammy has 9 more grapes than Heidi. Gina has 95 fewer grapes than Sam. Heidi has 90 fewer grapes than Frank. Cindy has 35 more grapes than Debbi. Derrek has 59 fewer grapes than Frank. Kim has 6 fewer grapes than Frank. Mia has 78 more grapes than Sam. Trent has 31 more grapes than Kristopher. Eugene has 15 fewer grapes than Heidi. Zack has 56 more grapes than Sam. Ivy has 34 more grapes than Debbi. Leta has 53 fewer grapes than Gina. Iola has 82 more grapes than Olive. Nancy has 38 more grapes than Sam. Xavier has 95 more grapes than Sam. Rob has 20 more grapes than Debbi. Peggy has 22 more grapes than Frank. Chad has 14 more grapes than Debbi. Kevin has 55 more grapes than Olive. Dylan has 52 more grapes than Sam. Heath has 51 fewer grapes than Olive. Judy has 98 fewer grapes than Frank. Nick has 74 more grapes than Debbi. Ivan has 72 more grapes than Sam. Sam has 32 more grapes than Frank. Alice has 76 more grapes than Olive. Quinn has 32 fewer grapes than Frank. Quentin has 65 more grapes than Frank. Finn has 37 fewer grapes than Sam. Callie has 68 more grapes than Frank. Debbi has 77 more grapes than Sam. Olivia has 48 more grapes than Frank. Bill has 78 fewer grapes than Olive. Olive has 11 grapes. Victor has 41 more grapes than Olive. Dan has 87 fewer grapes than Debbi. Bob has 53 fewer grapes than Debbi. Ursula has 8 more grapes than Sam. Maleah has 38 fewer grapes than Debbi. Kacey has 90 more grapes than Olive.\nQuestion: How many grapes does Chad have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Olive has 11 grapes, and Frank has 59 fewer grapes than Olive. So, Frank has 11-59=-48 grapes.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Frank has -48 grapes, and Sam has 32 more grapes than Frank. So, Sam has -48+32=-16 grapes.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Sam has -16 grapes, and Debbi has 77 more grapes than Sam. So, Debbi has -16+77=61 grapes.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Debbi has 61 grapes, and Chad has 14 more grapes than Debbi. So, Chad has 61+14=75 grapes.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The final answer is 75.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Yvonne has 36 more pencils than Larry. Judy has 50 fewer pencils than Quinn. Ursula has 69 fewer pencils than Ana. Carol has 43 more pencils than Quinn. Dan has 30 more pencils than Larry. Zoe has 57 more pencils than Ana. Jack has 41 more pencils than Ana. Yvonne's classmate has 28 fewer pencils than Quinn. Ivan has 26 fewer pencils than Quinn. Rob has 12 more pencils than Ana. Quinn has 45 fewer pencils than Ursula. Olive has 84 more pencils than Quinn. Yvonne's grandparent has 48 more pencils than Ana. Lance has 28 fewer pencils than Quinn. Xavier has 58 more pencils than Ana. Cathy has 33 fewer pencils than Yvonne's father. Bill has 58 fewer pencils than Ana. Emma has 43 more pencils than Ana. Zack has 19 more pencils than Larry. Eve has 3 fewer pencils than Larry. Trent has 98 more pencils than Yvonne's father. Nancy has 15 more pencils than Quinn. Amy has 89 fewer pencils than Larry. Tina has 43 more pencils than Ursula. Ana has 34 pencils. Yvonne's father has 100 fewer pencils than Ursula. Paul has 12 fewer pencils than Ursula. Cindy has 38 more pencils than Larry. Sybil has 39 more pencils than Larry. Sam has 46 fewer pencils than Ursula. Ivy has 91 more pencils than Quinn. Hank has 29 more pencils than Larry. Mallory has 72 more pencils than Ana. Frank has 27 more pencils than Quinn. Ruth has 37 fewer pencils than Ursula. Yvonne's friend has 64 more pencils than Larry. Kim has 2 fewer pencils than Larry. Alice has 11 fewer pencils than Ursula. Ben has 98 fewer pencils than Yvonne's classmate. Larry has 51 more pencils than Quinn. Nick has 96 fewer pencils than Yvonne's grandparent. Dylan has 40 fewer pencils than Ursula. Olivia has 94 fewer pencils than Yvonne's classmate. Victor has 41 more pencils than Ursula. Walter has 31 fewer pencils than Yvonne's grandparent. Mia has 51 fewer pencils than Ana. Heidi has 62 fewer pencils than Ursula.\nQuestion: How many pencils does Yvonne have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Ana has 34 pencils, and Ursula has 69 fewer pencils than Ana. So, Ursula has 34-69=-35 pencils.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Ursula has -35 pencils, and Quinn has 45 fewer pencils than Ursula. So, Quinn has -35-45=-80 pencils.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Quinn has -80 pencils, and Larry has 51 more pencils than Quinn. So, Larry has -80+51=-29 pencils.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Larry has -29 pencils, and Yvonne has 36 more pencils than Larry. So, Yvonne has -29+36=7 pencils.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The final answer is 7.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Peggy has 64 fewer pencils than Ana. Eugene has 11 more pencils than Alton. Debbi has 8 more pencils than Finn. Nancy has 97 more pencils than Finn. Dave has 96 more pencils than Olivia. Judy has 33 fewer pencils than Finn. Sybil has 47 more pencils than Alton. Brad has 9 fewer pencils than Ana. Ed has 17 more pencils than Finn. Jill has 98 fewer pencils than Finn. Finn has 21 more pencils than Alton. Ana has 23 fewer pencils than Olivia. Zack has 31 fewer pencils than Alton. Chad has 81 fewer pencils than Olivia. Olivia has 72 pencils. Ursula has 23 more pencils than Olivia. Aliyah has 65 more pencils than Alton. Kristopher has 76 fewer pencils than Finn. Xavier has 43 fewer pencils than Olivia. Franklyn has 70 more pencils than Alton. Jake has 3 more pencils than Alton. Yvonne has 79 fewer pencils than Peggy. Emery has 18 more pencils than Olivia. Carol has 18 more pencils than Ana. Dan has 47 fewer pencils than Finn. Dylan has 32 more pencils than Ana. Jack has 98 fewer pencils than Alton. Rob has 70 more pencils than Ana. Kim has 47 fewer pencils than Alton. Brande has 52 more pencils than Finn. Sam has 100 fewer pencils than Peggy. Iola has 24 fewer pencils than Ana. Cathy has 78 more pencils than Alton. Mia has 55 fewer pencils than Dave. Quentin has 13 more pencils than Ana. Alton has 63 more pencils than Ana. Bill has 36 more pencils than Eugene. Derrek has 85 more pencils than Finn. Mallory has 87 fewer pencils than Olivia. Bob has 92 fewer pencils than Dave. Grace has 6 fewer pencils than Ana. Tina has 6 more pencils than Ana. Heath has 95 more pencils than Eugene. Ivy has 29 more pencils than Finn. Paul has 26 fewer pencils than Olivia. Heidi has 11 more pencils than Olivia. Nick has 42 more pencils than Olivia.\nQuestion: How many pencils does Kristopher have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Olivia has 72 pencils, and Ana has 23 fewer pencils than Olivia. So, Ana has 72-23=49 pencils.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Ana has 49 pencils, and Alton has 63 more pencils than Ana. So, Alton has 49+63=112 pencils.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Alton has 112 pencils, and Finn has 21 more pencils than Alton. So, Finn has 112+21=133 pencils.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Finn has 133 pencils, and Kristopher has 76 fewer pencils than Finn. So, Kristopher has 133-76=57 pencils.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The final answer is 57.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Context: Grace has 54 more bananas than Kevin. Kevin has 54 fewer bananas than Zoe. Ana's classmate has 8 more bananas than Sam. Nick has 22 more bananas than Trent. Alice has 80 fewer bananas than Trent. Paul has 81 more bananas than Ana's mother. Rob has 44 more bananas than Zoe. Victor has 92 fewer bananas than Sam. Larry has 29 more bananas than Trent. Walter has 18 fewer bananas than Sam. Mallory has 89 more bananas than Kevin. Dan has 95 more bananas than Zoe. Emma has 79 more bananas than Trent. Tina has 16 fewer bananas than Trent. Dylan has 5 fewer bananas than Kevin. Ana has 97 more bananas than Sam. Zack has 70 more bananas than Zoe. Hank has 85 more bananas than Kevin. Cindy has 15 more bananas than Kevin. Frank has 36 more bananas than Zoe. Cathy has 78 more bananas than Sam. Yvonne has 95 more bananas than Sam. Zoe has 39 more bananas than Trent. Ivy has 78 more bananas than Ana's son. Heidi has 30 fewer bananas than Kevin. Ana's father has 44 more bananas than Trent. Judy has 96 more bananas than Zoe. Ana's mother has 83 more bananas than Kevin. Jack has 81 fewer bananas than Zoe. Gina has 40 more bananas than Sam. Xavier has 6 fewer bananas than Ana's father. Carol has 66 fewer bananas than Sam. Dave has 24 fewer bananas than Trent. Ana's son has 91 more bananas than Zoe. Ivan has 92 fewer bananas than Ana's mother. Wendy has 37 more bananas than Trent. Vince has 79 fewer bananas than Sam. Eve has 95 more bananas than Zoe. Kim has 84 more bananas than Sam. Sybil has 14 fewer bananas than Kevin. Ursula has 33 fewer bananas than Kevin. Sam has 98 more bananas than Kevin. Olivia has 28 fewer bananas than Ana's son. Bill has 39 fewer bananas than Ana's father. Finn has 34 fewer bananas than Zoe. Trent has 10 bananas. Olive has 87 more bananas than Trent.\nQuestion: How many bananas does Ana have?",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Trent has 10 bananas, and Zoe has 39 more bananas than Trent. So, Zoe has 10+39=49 bananas.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Zoe has 49 bananas, and Kevin has 54 fewer bananas than Zoe. So, Kevin has 49-54=-5 bananas.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Kevin has -5 bananas, and Sam has 98 more bananas than Kevin. So, Sam has -5+98=93 bananas.",
          "type": "text"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "text": "Sam has 93 bananas, and Ana has 97 more bananas than Sam. So, Ana has 93+97=190 bananas.",
          "type": "text"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "text": "The final answer is 190.",
          "type": "text"
        }
      ]
    },
  ]
    elif args.prompt_type == "overlap":
        prompt = [
            {
            "role": "system",
            "content": "Answer the context question according to the following example."
            },
            {
            "role": "user",
            "content": "Context: If Xavier is smart, then Rob is not clever. If Mallory is not witty, then Rob is not clever. Walter is not tall. Rob is pretty. Ivan is not handsome. If Ivan is not handsome, then Quentin is cool. If Rob is pretty, then Rob is not clever. If Walter is not tall, then Yvonne is handsome.\nQuestion: Rob is not clever?"
            },
            {
            "role": "assistant",
            "content": "Rob is pretty. If Rob is pretty, then Rob is not clever. Rob is not clever. The final answer is True."
            },
            {
            "role": "user",
            "content": "Context: If Ivan is hungry, then Ivan is wonderful. If Dave is not wonderful, then Ivan is not cute. If Eve is not beautiful, then Grace is nice. If Ivan is not kind, then Ivan is not cute. If Zoe is smart, then Dave is nice. If Heidi is youthful, then Ivan is not cute. If Kevin is honest, then Carol is ill. If Rob is pretty, then Grace is not nice. Kevin is honest. If Zoe is not nice, then Heidi is youthful. If Grace is not nice, then Dave is not wonderful. Eve is not beautiful. If Grace is funny, then Zoe is not nice. If Carol is ill, then Zoe is smart. Ivan is hungry. If Grace is nice, then Grace is tall. If Ivan is wonderful, then Ivan is not kind. If Grace is tall, then Trent is wonderful.\nQuestion: Ivan is cute?"
            },
            {
            "role": "assistant",
            "content": "Ivan is hungry. If Ivan is hungry, then Ivan is wonderful. Ivan is wonderful. If Ivan is wonderful, then Ivan is not kind. Ivan is not kind. If Ivan is not kind, then Ivan is not cute. Ivan is not cute. The final answer is False."
            },
            {
            "role": "user",
            "content": "Context: If Judy is not good, then Eve is cute. If Yvonne is handsome, then Yvonne is not pretty. Trent is rich. If Eve is cute, then Yvonne is cute. Eve is ill. If Yvonne is not pretty, then Yvonne is cute. If Eve is ill, then Walter is ill. If Trent is rich, then Olivia is not handsome. Yvonne is handsome. If Xavier is funny, then Kevin is tall. If Olivia is not handsome, then Dave is not youthful. If Kevin is tall, then Yvonne is cute. If Walter is ill, then Dave is not good.\nQuestion: Yvonne is cute?"
            },
            {
            "role": "assistant",
            "content": "Yvonne is handsome. If Yvonne is handsome, then Yvonne is not pretty. Yvonne is not pretty. If Yvonne is not pretty, then Yvonne is cute. Yvonne is cute. The final answer is True."
            },
            {
            "role": "user",
            "content": "Context: If Peggy is not beautiful, then Trent is clever. If Walter is rich, then Ivan is smart. If Kevin is clever, then Trent is not funny. If Ivan is not tall, then Ivan is not smart. If Xavier is ill, then Olivia is not funny. If Eve is youthful, then Alice is handsome. Bob is not funny. If Ivan is cute, then Ivan is funny. If Alice is handsome, then Carol is not cute. If Ivan is funny, then Ivan is tall. If Ursula is not honest, then Ivan is not smart. If Alice is not funny, then Peggy is not beautiful. Kevin is clever. If Ivan is tall, then Ivan is not tall. If Mallory is funny, then Ursula is not honest. If Bob is not funny, then Alice is not funny. If Trent is clever, then Victor is tall. Ivan is cute. If Quentin is not honest, then Mallory is funny. If Rob is not cool, then Xavier is ill. If Walter is hungry, then Quentin is not honest. If Carol is not cute, then Walter is rich. If Trent is not funny, then Rob is not cool.\nQuestion: Ivan is smart?"
            },
            {
            "role": "assistant",
            "content": "Ivan is cute. If Ivan is cute, then Ivan is funny. Ivan is funny. If Ivan is funny, then Ivan is tall. Ivan is tall. If Ivan is tall, then Ivan is not tall. Ivan is not tall. If Ivan is not tall, then Ivan is not smart. Ivan is not smart. The final answer is False."
            },
            {
            "role": "user",
            "content": "Context: Nancy is not beautiful. Dave is not cool. Heidi is rich.\nQuestion: Dave is cool?"
            },
            {
            "role": "assistant",
            "content": "Dave is not cool. The final answer is False."
            }
        ]
    elif args.prompt_type == "negative":
        prompt = [
            {
                "role": "system",
                "content": "Answer the context question according to the following example.\n\n"
            },
            {
                "role": "user",
                "content": "Context: If Quentin is youthful, then Zoe is not ill. If Olivia is small, then Mallory is wonderful. If Sybil is not wonderful, then Frank is not good. If Grace is witty, then Quentin is youthful. If Nancy is cute, then Olivia is small. If Walter is cool, then Grace is witty. If Peggy is not pretty, then Walter is not witty. If Trent is youthful, then Walter is cute. If Mallory is wonderful, then Zoe is ill. If Olivia is ill, then Dave is cool. If Yvonne is handsome, then Xavier is youthful. If Trent is smart, then Olivia is ill. If Dave is cool, then Trent is youthful. If Sybil is tall, then Walter is cool. If Walter is not witty, then Sybil is not wonderful. If Frank is not good, then Zoe is not ill. If Xavier is youthful, then Heidi is witty. If Judy is small, then Xavier is witty. Peggy is not pretty. If Sybil is beautiful, then Nancy is cute. Trent is smart. If Xavier is witty, then Yvonne is handsome. Judy is small.\nQuestion: Zoe is ill?"
            },
            {
                "role": "assistant",
                "content": "Peggy is not pretty. If Peggy is not pretty, then Walter is not witty. Walter is not witty. If Walter is not witty, then Sybil is not wonderful. Sybil is not wonderful. If Sybil is not wonderful, then Frank is not good. Frank is not good. If Frank is not good, then Zoe is not ill. Zoe is not ill. The final answer is False."
            },
            {
                "role": "user",
                "content": "Context: Trent is hungry. If Grace is not handsome, then Walter is not cute. Frank is tall. If Judy is funny, then Heidi is not funny. If Heidi is rich, then Yvonne is pretty. If Quentin is pretty, then Judy is funny. If Trent is hungry, then Yvonne is handsome. If Frank is tall, then Larry is tall. Grace is not handsome. If Larry is tall, then Ursula is good. If Yvonne is handsome, then Walter is beautiful. If Yvonne is pretty, then Heidi is funny. If Walter is not cute, then Heidi is not funny.\nQuestion: Heidi is funny?"
            },
            {
                "role": "assistant",
                "content": "Grace is not handsome. If Grace is not handsome, then Walter is not cute. Walter is not cute. If Walter is not cute, then Heidi is not funny. Heidi is not funny. The final answer is False."
            },
            {
                "role": "user",
                "content": "Context: If Zoe is not cute, then Mallory is not pretty. If Mallory is good, then Sybil is kind. If Ivan is beautiful, then Peggy is zany. Dave is youthful. If Frank is not cool, then Zoe is not cute. If Victor is witty, then Mallory is good. If Mallory is ill, then Xavier is hungry. Frank is not cool. Heidi is cool. If Nancy is witty, then Peggy is not zany. If Mallory is hungry, then Trent is good. If Heidi is cool, then Peggy is tall. If Trent is good, then Ivan is beautiful. If Mallory is not pretty, then Peggy is not zany. If Xavier is small, then Quentin is ill. If Peggy is tall, then Mallory is ill. If Dave is youthful, then Victor is witty. If Quentin is ill, then Nancy is witty.\nQuestion: Peggy is not zany?"
            },
            {
                "role": "assistant",
                "content": "Frank is not cool. If Frank is not cool, then Zoe is not cute. Zoe is not cute. If Zoe is not cute, then Mallory is not pretty. Mallory is not pretty. If Mallory is not pretty, then Peggy is not zany. Peggy is not zany. The final answer is True."
            },
            {
                "role": "user",
                "content": "Context: Bob is smart. Carol is not funny. Yvonne is clever.\nQuestion: Carol is funny?\n"
            },
            {
                "role": "assistant",
                "content": "Carol is not funny. The final answer is False."
            },
            {
                "role": "user",
                "content": "Context: Olivia is rich. Alice is not honest. If Zoe is wonderful, then Frank is not hungry. If Carol is tall, then Frank is not hungry. If Olivia is rich, then Peggy is small. If Alice is not honest, then Frank is not hungry. Ivan is kind. If Ivan is kind, then Olivia is wonderful.\nQuestion: Frank is not hungry?"
            },
            {
                "role": "assistant",
                "content": "Alice is not honest. If Alice is not honest, then Frank is not hungry. Frank is not hungry. The final answer is True."
            }
        ]
    elif args.prompt_type == "position":
        prompt = [
            {
                "role": "system",
                "content": "Answer the context question according to the following example."
            },
            {
                "role": "user",
                "content": "Context: Nancy is not tall. If Nancy is not tall, then Olivia is not witty. If Olivia is not witty, then Eve is youthful. If Eve is youthful, then Dave is smart. If Heidi is beautiful, then Frank is not witty. If Larry is not beautiful, then Dave is not smart. If Dave is not good, then Larry is handsome. If Frank is not witty, then Larry is not beautiful. If Eve is not smart, then Quentin is not pretty. Bob is beautiful. If Quentin is not pretty, then Grace is rich. If Peggy is not pretty, then Rob is funny. If Bob is beautiful, then Eve is not smart. Mallory is clever. If Peggy is not smart, then Dave is smart. If Mallory is clever, then Peggy is not pretty. If Larry is handsome, then Peggy is not smart. If Rob is funny, then Trent is rich.\nQuestion: Dave is smart?"
            },
            {
                "role": "assistant",
                "content": "Nancy is not tall. If Nancy is not tall, then Olivia is not witty. Olivia is not witty. If Olivia is not witty, then Eve is youthful. Eve is youthful. If Eve is youthful, then Dave is smart. Dave is smart. The final answer is True."
            },
            {
                "role": "user",
                "content": "Context: Xavier is hungry. If Xavier is hungry, then Xavier is not handsome. If Xavier is not handsome, then Rob is not cute. If Rob is not cute, then Carol is not smart. If Carol is not smart, then Ursula is not smart. If Trent is handsome, then Mallory is not witty. Grace is not pretty. If Judy is pretty, then Quentin is good. If Trent is youthful, then Grace is nice. If Grace is not pretty, then Judy is pretty. If Sybil is pretty, then Dave is not smart. If Bob is pretty, then Grace is not rich. Trent is youthful. If Grace is nice, then Bob is pretty. If Eve is rich, then Nancy is wonderful. If Grace is not rich, then Nancy is not ill. If Dave is not smart, then Heidi is not wonderful. If Victor is not kind, then Ursula is not smart. If Heidi is not wonderful, then Sybil is not kind. If Quentin is good, then Eve is rich. If Walter is not cute, then Victor is not kind. If Mallory is not witty, then Walter is not cute. If Sybil is not kind, then Ursula is not smart.\nQuestion: Ursula is not smart?"
            },
            {
                "role": "assistant",
                "content": "Xavier is hungry. If Xavier is hungry, then Xavier is not handsome. Xavier is not handsome. If Xavier is not handsome, then Rob is not cute. Rob is not cute. If Rob is not cute, then Carol is not smart. Carol is not smart. If Carol is not smart, then Ursula is not smart. Ursula is not smart. The final answer is True."
            },
            {
                "role": "user",
                "content": "Context: Larry is tall. If Larry is tall, then Kevin is not kind. Olivia is beautiful. Yvonne is tall. If Olivia is beautiful, then Ursula is honest. If Judy is good, then Kevin is kind. If Yvonne is tall, then Olivia is not wonderful. If Victor is not nice, then Kevin is not kind.\nQuestion: Kevin is kind?"
            },
            {
                "role": "assistant",
                "content": "Larry is tall. If Larry is tall, then Kevin is not kind. Kevin is not kind. The final answer is False."
            },
            {
                "role": "user",
                "content": "Context: Dave is not clever. Quentin is not handsome. Olivia is not wonderful.\nQuestion: Dave is not clever?"
            },
            {
                "role": "assistant",
                "content": "Dave is not clever. The final answer is True."
            },
            {
                "role": "user",
                "content": "Context: Judy is not cool. If Judy is not cool, then Yvonne is hungry. If Yvonne is hungry, then Xavier is not good. If Judy is not smart, then Frank is kind. If Dave is not cool, then Walter is wonderful. If Ivan is cute, then Alice is not pretty. Judy is not smart. If Olivia is not tall, then Dave is not cool. Olivia is not tall. If Rob is not cute, then Bob is not hungry. If Bob is not hungry, then Xavier is good. If Frank is kind, then Ivan is nice. If Alice is not pretty, then Xavier is good.\nQuestion: Xavier is good?"
            },
            {
                "role": "assistant",
                "content": "Judy is not cool. If Judy is not cool, then Yvonne is hungry. Yvonne is hungry. If Yvonne is hungry, then Xavier is not good. Xavier is not good. The final answer is False."
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
            response = module.send(context=inputs[index],answers=outputs[index][:args.depth])

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
            f.write("Pred Reasoning Steps:\n")
            f.write(response+"\n")
            f.write("------------------\n")


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
