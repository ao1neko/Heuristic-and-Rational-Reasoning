import argparse
from cmath import e, log
from operator import mod
import numpy as np
import torch
import torch.optim as optim
from distutils.util import strtobool
import random
from torch.utils.data.dataset import Subset
from pathlib import Path
from tqdm import tqdm
from torch.utils.data import Dataset
import numpy as np
import os
from typing import List, Dict, Set
import string
import copy
import json
import math
from src.data.formal_language.data_class import LogicInstance, Node, Instance, LogicDataset

class Sentence():
    def __init__(self, name, number, object:str="apples", negative="has") -> None:
        self.name = name
        self.number = number
        self.object = object
        self.negative = negative
    
    def __str__(self) -> str:
        return f"{self.name} {self.negative} {str(self.number)} {self.object}."


class RelationalSentence(Sentence):
    def __init__(self,name,number,relate_name:str,object:str="apples",operator:str="more",negative="has") -> None:
        super().__init__(name,number,object=object,negative=negative)
        self.operator = operator
        self.relate_name = relate_name

    def __str__(self) -> str:
        return f"{self.name} {self.negative} {str(self.number)} {self.operator} {self.object} than {self.relate_name}."

class Instance():
    def __init__(self,) -> None:
        self.name_set = ["Alice","Bob","Carol","Dave","Eve","Frank","Grace","Heidi","Ivan","Judy","Kevin","Larry","Mallory","Nancy","Olivia","Peggy","Quentin","Rob","Sybil","Trent","Ursula","Victor","Walter","Xavier","Yvonne","Zoe"]
        self.objects = ["apples","bananas","grapes","pencils","books"]
        self.sentences, self.question, self.answer, self.gold_outputs, self.not_gold_outputs,self.gold_positions,self.not_gold_positions = self._make_instance()
        

    def _get_random_names(self, name_num) -> str:
        names = random.sample(self.name_set, k=name_num)
        return names

    def _make_instance(self, name_num:int=19) -> List[Sentence]:
        names = self._get_random_names(name_num)
        object = random.choice(self.objects)
        
        
        #0,1,3,7,15
        sentences = []
        sentences.append(Sentence(names[0],random.randint(0,100),object=object))
        sentences += self._make_minimum_tree(names[1],names[2],names[0],object=object)
        sentences += self._make_minimum_tree(names[3],names[4],names[1],object=object)
        sentences += self._make_minimum_tree(names[5],names[6],names[2],object=object)
        sentences += self._make_minimum_tree(names[7],names[8],names[3],object=object)
        sentences += self._make_minimum_tree(names[9],names[10],names[4],object=object)
        sentences += self._make_minimum_tree(names[11],names[12],names[5],object=object)
        sentences += self._make_minimum_tree(names[13],names[14],names[6],object=object)
        sentences += self._make_minimum_tree(names[15],names[16],names[7],object=object)
        sentences += self._make_minimum_tree(names[17],names[18],names[8],object=object)
        
        
        question = f"How many {object} does {names[15]} have?"
        gold_outputs = []
        
        if sentences[1].operator == "more":
            number_of_AB = sentences[0].number + sentences[1].number
            gold_outputs.append(f"{str(sentences[0])[:-1]}, and {str(sentences[1])} So, {names[1]} has {sentences[0].number}+{sentences[1].number}={number_of_AB} {object}.")
        elif sentences[1].operator == "less":
            number_of_AB = sentences[0].number - sentences[1].number
            gold_outputs.append(f"{str(sentences[0])[:-1]}, and {str(sentences[1])} So, {names[1]} has {sentences[0].number}-{sentences[1].number}={number_of_AB} {object}.")
        
        if sentences[3].operator == "more":
            number_of_BC = number_of_AB + sentences[3].number
            gold_outputs.append(f"{names[1]} has {number_of_AB} {object}, and {str(sentences[3])} So, {names[3]} has {number_of_AB}+{sentences[3].number}={number_of_BC} {object}.")
        elif sentences[3].operator == "less":
            number_of_BC = number_of_AB - sentences[3].number
            gold_outputs.append(f"{names[1]} has {number_of_AB} {object}, and {str(sentences[3])} So, {names[3]} has {number_of_AB}-{sentences[3].number}={number_of_BC} {object}.")
        if sentences[7].operator == "more":
            number_of_CD = number_of_BC + sentences[7].number
            gold_outputs.append(f"{names[3]} has {number_of_BC} {object}, and {str(sentences[7])} So, {names[7]} has {number_of_BC}+{sentences[7].number}={number_of_CD} {object}.")
        elif sentences[7].operator == "less":
            number_of_CD = number_of_BC - sentences[7].number
            gold_outputs.append(f"{names[3]} has {number_of_BC} {object}, and {str(sentences[7])} So, {names[7]} has {number_of_BC}-{sentences[7].number}={number_of_CD} {object}.")
        if sentences[15].operator == "more":
            number_of_DE = number_of_CD + sentences[15].number
            gold_outputs.append(f"{names[7]} has {number_of_CD} {object}, and {str(sentences[15])} So, {names[15]} has {number_of_CD}+{sentences[15].number}={number_of_DE} {object}.")
        elif sentences[15].operator == "less":
            number_of_DE = number_of_CD - sentences[15].number
            gold_outputs.append(f"{names[7]} has {number_of_CD} {object}, and {str(sentences[15])} So, {names[15]} has {number_of_CD}-{sentences[15].number}={number_of_DE} {object}.")
            
        gold_outputs.append(f"The final answer is {number_of_CD}.")
        
        not_gold_outputs = [
            f"{str(sentences[0])[:-1]}, and {str(sentences[2])} So, {names[2]} has x {object}.",
            f"{names[1]} has x {object}, and {str(sentences[4])} So, {names[4]} has x {object}.",
            f"{names[3]} has x {object}, and {str(sentences[8])} So, {names[8]} has x {object}.",
            f"{names[7]} has x {object}, and {str(sentences[16])} So, {names[16]} has x {object}."
        ]
        shuffle_sentences = copy.deepcopy(sentences)
        random.shuffle(shuffle_sentences)
        gold_positions = []
        not_gold_positions = []
        shuffle_sentences = [str(s) for s in shuffle_sentences]
        for gold in [str(sentences[0]),str(sentences[1]),str(sentences[3]),str(sentences[7])]:
            gold_positions.append(shuffle_sentences.index(gold))
        for not_gold in [str(sentences[2]),str(sentences[4]),str(sentences[8]),str(sentences[16])]:
            not_gold_positions.append(shuffle_sentences.index(not_gold))
        return shuffle_sentences, question, number_of_CD, gold_outputs, not_gold_outputs, gold_positions, not_gold_positions
    
    def _make_minimum_tree(self, name1, name2, relate_name:str,object:str="apples") -> List[Sentence]:
        sentences = []
        sentences.append(RelationalSentence(name1,random.randint(0,100),relate_name=relate_name,operator=random.choice(["more","less"]),object=object))
        sentences.append(RelationalSentence(name2,random.randint(0,100),relate_name=relate_name,operator=random.choice(["more","less"]),object=object))
        return sentences


class OverlapInstance(Instance):
    def __init__(self,) -> None:
        self.name_set = ["Alice","Bob","Carol","Dave","Eve","Frank","Grace","Heidi","Ivan","Judy","Kevin","Larry","Mallory","Nancy","Olivia","Peggy","Quentin","Rob","Sybil","Trent","Ursula","Victor","Walter","Xavier","Yvonne","Zoe"]
        random.shuffle(self.name_set)
        self.question_name = self.name_set.pop()
        self.similar_name = ["'s mother","'s father","'s son","'s neighborhood"]
        random.shuffle(self.similar_name)
        self.objects = ["apples","bananas","grapes","pencils","books"]
        self.sentences, self.question, self.answer, self.gold_outputs, self.not_gold_outputs,self.gold_positions,self.not_gold_positions = self._make_instance()

    def _get_random_names(self, name_num) -> str:
        names = random.sample(self.name_set, k=name_num)
        return names

    def _make_instance(self, name_num:int=19) -> List[Sentence]:
        names = self._get_random_names(name_num)
        name2 = self.question_name + self.similar_name.pop()
        name4 = self.question_name + self.similar_name.pop()
        name8 = self.question_name + self.similar_name.pop()
        object = random.choice(self.objects)
        #name8 = self.question_name + self.similar_name.pop()
        
        
        #0,1,3,7,15
        sentences = []
        sentences.append(Sentence(names[0],random.randint(0,5),object=object))
        sentences += self._make_minimum_tree(names[1],name2,names[0],object=object)
        sentences += self._make_minimum_tree(names[3],name4,names[1],object=object)
        sentences += self._make_minimum_tree(names[5],names[6],name2,object=object)
        sentences += self._make_minimum_tree(names[7],name8,names[3],object=object)
        sentences += self._make_minimum_tree(names[9],names[10],name4,object=object)
        sentences += self._make_minimum_tree(names[11],names[12],names[5],object=object)
        sentences += self._make_minimum_tree(names[13],names[14],names[6],object=object)
        sentences += self._make_minimum_tree(self.question_name,names[16],names[7],object=object)
        sentences += self._make_minimum_tree(names[17],names[18],name8,object=object)
        
        
        question = f"How many {object} does {self.question_name} have?"
        
        gold_outputs = []
        
        if sentences[1].operator == "more":
            number_of_AB = sentences[0].number + sentences[1].number
            gold_outputs.append(f"{str(sentences[0])[:-1]}, and {str(sentences[1])} So, {names[1]} has {sentences[0].number}+{sentences[1].number}={number_of_AB} {object}.")
        elif sentences[1].operator == "less":
            number_of_AB = sentences[0].number - sentences[1].number
            gold_outputs.append(f"{str(sentences[0])[:-1]}, and {str(sentences[1])} So, {names[1]} has {sentences[0].number}-{sentences[1].number}={number_of_AB} {object}.")
        
        if sentences[3].operator == "more":
            number_of_BC = number_of_AB + sentences[3].number
            gold_outputs.append(f"{names[1]} has {number_of_AB} {object}, and {str(sentences[3])} So, {names[3]} has {number_of_AB}+{sentences[3].number}={number_of_BC} {object}.")
        elif sentences[3].operator == "less":
            number_of_BC = number_of_AB - sentences[3].number
            gold_outputs.append(f"{names[1]} has {number_of_AB} {object}, and {str(sentences[3])} So, {names[3]} has {number_of_AB}-{sentences[3].number}={number_of_BC} {object}.")
            
        if sentences[7].operator == "more":
            number_of_CD = number_of_BC + sentences[7].number
            gold_outputs.append(f"{names[3]} has {number_of_BC} {object}, and {str(sentences[7])} So, {names[7]} has {number_of_BC}+{sentences[7].number}={number_of_CD} {object}.")
        elif sentences[7].operator == "less":
            number_of_CD = number_of_BC - sentences[7].number
            gold_outputs.append(f"{names[3]} has {number_of_BC} {object}, and {str(sentences[7])} So, {names[7]} has {number_of_BC}-{sentences[7].number}={number_of_CD} {object}.")
        if sentences[15].operator == "more":
            number_of_DE = number_of_CD + sentences[15].number
            gold_outputs.append(f"{names[7]} has {number_of_CD} {object}, and {str(sentences[15])} So, {self.question_name} has {number_of_CD}+{sentences[15].number}={number_of_DE} {object}.")
        elif sentences[15].operator == "less":
            number_of_DE = number_of_CD - sentences[15].number
            gold_outputs.append(f"{names[7]} has {number_of_CD} {object}, and {str(sentences[15])} So, {self.question_name} has {number_of_CD}-{sentences[15].number}={number_of_DE} {object}.")
        
        
        gold_outputs.append(f"The final answer is {number_of_DE}.")
        not_gold_outputs = [
            f"{str(sentences[0])[:-1]}, and {str(sentences[2])} So, {name2} has x {object}.",
            f"{names[1]} has x {object}, and {str(sentences[4])} So, {name4} has x {object}.",
            f"{names[3]} has x {object}, and {str(sentences[8])} So, {name8} has x {object}.",
        ]
        shuffle_sentences = copy.deepcopy(sentences)
        random.shuffle(shuffle_sentences)
        shuffle_sentences = [str(s) for s in shuffle_sentences]
        return shuffle_sentences, question, number_of_DE, gold_outputs, not_gold_outputs, [], []

class NegativeInstance(Instance):
    def _make_minimum_tree(self, name1, name2, relate_name:str,object:str="apples") -> List[Sentence]:
        sentences = []
        sentences.append(RelationalSentence(name1,random.randint(0,5),relate_name=relate_name,operator=random.choice(["more","less"]),object=object, negative="has"))
        sentences.append(RelationalSentence(name2,random.randint(0,5),relate_name=relate_name,operator=random.choice(["more","less"]),object=object, negative="doesn't have"))
        return sentences

class PositionalInstance(Instance):
    def _make_instance(self, name_num:int=19) -> List[Sentence]:
        names = self._get_random_names(name_num)
        object = random.choice(self.objects)
        
        #0,1,3,7,15
        sentences = []
        sentences.append(Sentence(names[0],random.randint(0,5),object=object))
        sentences += self._make_minimum_tree(names[5],names[6],names[2],object=object)
        sentences += self._make_minimum_tree(names[9],names[10],names[4],object=object)
        sentences += self._make_minimum_tree(names[11],names[12],names[5],object=object)
        sentences += self._make_minimum_tree(names[13],names[14],names[6],object=object)
        sentences += self._make_minimum_tree(names[17],names[18],names[8],object=object)
        shuffle_sentences = copy.deepcopy(sentences)
        
        random.shuffle(shuffle_sentences)
        sentence1 = self._make_minimum_tree(names[1],names[2],names[0],object=object)
        i0,i1 = sorted(random.sample(range(len(shuffle_sentences)+2),k=2))
        shuffle_sentences.insert(i0,sentence1[1])
        shuffle_sentences.insert(i1,sentence1[0])
        sentence2 = self._make_minimum_tree(names[3],names[4],names[1],object=object)
        i0,i1 = sorted(random.sample(range(len(shuffle_sentences)+2),k=2))
        shuffle_sentences.insert(i0,sentence2[1])
        shuffle_sentences.insert(i1,sentence2[0])
        sentence3 = self._make_minimum_tree(names[7],names[8],names[3],object=object)
        i0,i1 = sorted(random.sample(range(len(shuffle_sentences)+2),k=2))
        shuffle_sentences.insert(i0,sentence3[1])
        shuffle_sentences.insert(i1,sentence3[0])
        sentence4 = self._make_minimum_tree(names[15],names[16],names[7],object=object)
        i0,i1 = sorted(random.sample(range(len(shuffle_sentences)+2),k=2))
        shuffle_sentences.insert(i0,sentence4[1])
        shuffle_sentences.insert(i1,sentence4[0])
        
        
        gold_outputs = []
        question = f"How many {object} does {names[15]} have?"
        if sentence1[0].operator == "more":
            number_of_AB = sentences[0].number + sentence1[0].number
            gold_outputs.append(f"{str(sentences[0])[:-1]}, and {str(sentence1[0])} So, {names[1]} has {sentences[0].number}+{sentence1[0].number}={number_of_AB} {object}.")
        elif sentence1[0].operator == "less":
            number_of_AB = sentences[0].number - sentence1[0].number
            gold_outputs.append(f"{str(sentences[0])[:-1]}, and {str(sentence1[0])} So, {names[1]} has {sentences[0].number}-{sentence1[0].number}={number_of_AB} {object}.")
        
        if sentence2[0].operator == "more":
            number_of_BC = number_of_AB + sentence2[0].number
            gold_outputs.append(f"{names[1]} has {number_of_AB} {object}, and {str(sentence2[0])} So, {names[3]} has {number_of_AB}+{sentence2[0].number}={number_of_BC} {object}.")
        elif sentence2[0].operator == "less":
            number_of_BC = number_of_AB - sentence2[0].number
            gold_outputs.append(f"{names[1]} has {number_of_AB} {object}, and {str(sentence2[0])} So, {names[3]} has {number_of_AB}-{sentence2[0].number}={number_of_BC} {object}.")
            
        if sentence3[0].operator == "more":
            number_of_CD = number_of_BC + sentence3[0].number
            gold_outputs.append(f"{names[3]} has {number_of_BC} {object}, and {str(sentence3[0])} So, {names[7]} has {number_of_BC}+{sentence3[0].number}={number_of_CD} {object}.")
        elif sentence3[0].operator == "less":
            number_of_CD = number_of_BC - sentence3[0].number
            gold_outputs.append(f"{names[3]} has {number_of_BC} {object}, and {str(sentence3[0])} So, {names[7]} has {number_of_BC}-{sentence3[0].number}={number_of_CD} {object}.")
        if sentence4[0].operator == "more":
            number_of_DE = number_of_CD + sentence4[0].number
            gold_outputs.append(f"{names[7]} has {number_of_CD} {object}, and {str(sentence4[0])} So, {names[15]} has {number_of_CD}+{sentence4[0].number}={number_of_DE} {object}.")
        elif sentence4[0].operator == "less":
            number_of_DE = number_of_CD - sentence4[0].number
            gold_outputs.append(f"{names[7]} has {number_of_CD} {object}, and {str(sentence4[0])} So, {names[15]} has {number_of_CD}-{sentence4[0].number}={number_of_DE} {object}.")
        
        gold_outputs.append(f"The final answer is {number_of_DE}.")
        not_gold_outputs = [
            f"{str(sentences[0])[:-1]}, and {str(sentence1[1])} So, {names[2]} has x {object}.",
            f"{names[1]} has x {object}, and {str(sentence2[1])} So, {names[4]} has x {object}.",
            f"{names[3]} has x {object}, and {str(sentence3[1])} So, {names[8]} has x {object}.",
            f"{names[7]} has x {object}, and {str(sentence4[1])} So, {names[16]} has x {object}."
        ]

        gold_positions = []
        not_gold_positions = []
        shuffle_sentences = [str(s) for s in shuffle_sentences]
        for gold in [str(sentences[0]),str(sentence1[0]),str(sentence2[0]),str(sentence3[0]),str(sentence4[0])]:
            gold_positions.append(shuffle_sentences.index(gold))
        for not_gold in [str(sentence1[1]),str(sentence2[1]),str(sentence3[1]),str(sentence4[1])]:
            not_gold_positions.append(shuffle_sentences.index(not_gold))
        return shuffle_sentences, question, number_of_DE, gold_outputs, not_gold_outputs, gold_positions, not_gold_positions



def main(args):
    seed=44
    random.seed(seed)
    np.random.seed(seed)
    
    os.makedirs(Path(args.output_file).parent, exist_ok=True)
    with open(Path(args.output_file),"w") as f:
        for _ in range(300):
            if args.data_type == "flat":
                instance = Instance()
            elif args.data_type == "overlap":
                instance = OverlapInstance()
            elif args.data_type == "negative":
                instance = NegativeInstance()
            elif args.data_type == "position":
                instance = PositionalInstance()
            sentences = " ".join([str(s) for s in instance.sentences])

            input = "Context: " + sentences+"\nQuestion: "+instance.question + "\n"
            
            json_data = {
                "input": input,
                "answer": instance.answer,
                "gold_outputs": instance.gold_outputs,
                "not_gold_outputs": instance.not_gold_outputs,
                "gold_positions": instance.gold_positions,
                "not_gold_positions": instance.not_gold_positions
            }
            f.write(json.dumps(json_data))
            f.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--output_file', default="save/test")
    parser.add_argument('--data_type', default="flat")
    args = parser.parse_args()
    main(args)
