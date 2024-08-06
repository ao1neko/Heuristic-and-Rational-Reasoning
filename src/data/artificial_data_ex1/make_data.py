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
    def __init__(self, name, number, object:str="apples",negative="has") -> None:
        self.name = name
        self.number = number
        self.object = object
        self.negative = negative
        
    def __str__(self) -> str:
        return f"{self.name} {self.negative} {str(self.number)} {self.object}."

class RelationalSentence(Sentence):
    def __init__(self,name,number,relate_name:str,object:str="apples",operator:str="more",negative:str="has",) -> None:
        super().__init__(name,number,object=object,negative=negative)
        self.operator = operator
        self.relate_name = relate_name

    def __str__(self) -> str:
        return f"{self.name} {self.negative} {str(self.number)} {self.operator} {self.object} than {self.relate_name}."


class Instance():
    def __init__(self,) -> None:
        self.name_set = ["Alice","Bob","Carol","Dave","Eve","Frank","Grace","Heidi","Ivan","Judy","Kevin","Larry","Mallory","Nancy","Olivia","Peggy","Quentin","Rob","Sybil","Trent","Ursula","Victor","Walter","Xavier","Yvonne","Zoe"]
        self.similar_name = ["'s mother","'s father","'s son","'s neighborhood"]
        self.objects = ["apples","bananas","grapes","pencils","books"]
        #self.sentences, self.overlap_sentences, self.negative_sentences, self.position_sentences, self.logic_sentences, self.question, self.gold_outputs, self.answer, self.logic_gold_outputs, self.logic_answer,self.sentence_p, self.sentence_overlap_p, self.redundant_number= self._make_instance()
        self.sentences, self.overlap_sentences, self.negative_sentences, self.position_sentences, self.question, self.gold_outputs, self.answer, self.sentence_p, self.sentence_overlap_p, self.redundant_number= self._make_instance()
        


    def _get_random_names(self, name_num) -> str:
        names = random.sample(self.name_set, k=name_num)
        return names

    def _make_instance(self, name_num:int=7) -> List[Sentence]:
        names = self._get_random_names(name_num)
        numbers = random.choices(range(100),k=7)
        sentences = []
        object = random.choice(self.objects)
        
        # sentences[0~5]
        sentences.append(Sentence(names[0],numbers[0],object=object))
        sentences += self._make_minimum_tree(names[1],names[0],num=numbers[1],object=object)
        sentences += self._make_minimum_tree(names[2],names[1],num=numbers[2],object=object)
        sentences += self._make_minimum_tree(names[3],names[2],num=numbers[3],object=object)
        #sentences += self._make_minimum_tree(names[5],names[4],num=numbers[5],object=object)
        #sentences += self._make_minimum_tree(names[6],names[5],num=numbers[6],object=object)
        
        #redundant_sentence = self._make_minimum_tree(names[4],names[0],num=numbers[4],object=object)[0]
        redundant_sentence = random.choice([self._make_minimum_tree(names[4],random.choice([names[0],names[1],names[2],names[3]]),num=numbers[4],object=object)[0],Sentence(names[4],numbers[4],object=object)])
        
        sentence_p = str(redundant_sentence)
        
        question = f"How many {object} does {names[3]} have?"
        gold_outputs, answer = self._make_gold_outputs(sentences,names,object=object)
        
        #logic_sentences = copy.deepcopy(sentences)
        #logic_sentences[2].relate_name = names[4]
        #logic_sentences[4].relate_name = names[1]
        #logic_gold_outputs, logic_answer = self._make_logic_gold_outputs(logic_sentences,names,redundant_sentence,object=object)
        
        """
        p = list(zip(sentences, logic_sentences))
        random.shuffle(p)
        sentences, logic_sentences = zip(*p)
        sentences = list(sentences)
        logic_sentences = list(logic_sentences)
        """
        
        random.shuffle(sentences)

        overlap_sentences = copy.deepcopy(sentences)
        negative_sentences = copy.deepcopy(sentences)
        position_sentences = copy.deepcopy(sentences)

        redundant_number = numbers[4]
        redundant_position = random.randint(1,4)
        #redundant_position = random.randint(1,5)
        position_position = random.randint(0,redundant_position-1)

        sentences.insert(redundant_position,copy.deepcopy(redundant_sentence))
        overlap_sentences.insert(redundant_position,copy.deepcopy(redundant_sentence))
        negative_sentences.insert(redundant_position,copy.deepcopy(redundant_sentence))
        position_sentences.insert(position_position,copy.deepcopy(redundant_sentence))
        #logic_sentences.insert(redundant_position,copy.deepcopy(redundant_sentence))

        similar_name = random.choice(self.similar_name)
        overlap_sentences[redundant_position].name = names[3] + similar_name
        sentence_overlap_p = str(overlap_sentences[redundant_position])
        negative_sentences[redundant_position].negative = "doesn't have"

        return sentences, overlap_sentences, negative_sentences, position_sentences, question, gold_outputs,answer, sentence_p, sentence_overlap_p,redundant_number
        #return sentences, overlap_sentences, negative_sentences, position_sentences, logic_sentences, question, gold_outputs,answer, logic_gold_outputs, logic_answer, sentence_p, sentence_overlap_p,redundant_number



    def _make_gold_outputs(self, sentences:List[Sentence],names:List[str],object:str) -> List[str]:
        if sentences[1].operator == "more":
            number_of_AB = sentences[0].number + sentences[1].number
        elif sentences[1].operator == "less":
            number_of_AB = sentences[0].number - sentences[1].number
        
        if sentences[2].operator == "more":
            number_of_BC = number_of_AB + sentences[2].number
        elif sentences[2].operator == "less":
            number_of_BC = number_of_AB - sentences[2].number
            
        if sentences[3].operator == "more":
            number_of_CD = number_of_BC + sentences[3].number
        elif sentences[3].operator == "less":
            number_of_CD = number_of_BC - sentences[3].number
        
        gold_outputs = [
            f"{str(sentences[0])[:-1]}, and {str(sentences[1])} So, {names[1]} has {number_of_AB} {object}.",
            f"{names[1]} has {number_of_AB} {object}, and {str(sentences[2])} So, {names[2]} has {number_of_BC} {object}.",
            f"{names[2]} has {number_of_BC} {object}, and {str(sentences[3])} So, {names[3]} has {number_of_CD} {object}.",
            f"The final answer is {number_of_CD}."
        ]
        answer = number_of_CD
        return gold_outputs, answer
    """
    def _make_logic_gold_outputs(self, sentences:List[Sentence],names:List[str],redundant_sentence:Sentence,object:str) -> List[str]:
        if redundant_sentence.operator == "more":
            number_of_AB = sentences[0].number + redundant_sentence.number
        elif redundant_sentence.operator == "less":
            number_of_AB = sentences[0].number - redundant_sentence.number
        
        if sentences[2].operator == "more":
            number_of_BC = number_of_AB + sentences[2].number
        elif sentences[2].operator == "less":
            number_of_BC = number_of_AB - sentences[2].number
            
        if sentences[3].operator == "more":
            number_of_CD = number_of_BC + sentences[3].number
        elif sentences[3].operator == "less":
            number_of_CD = number_of_BC - sentences[3].number
        
        gold_outputs = [
            f"{str(sentences[0])[:-1]}, and {str(redundant_sentence)} So, {names[4]} has {number_of_AB} {object}.",
            f"{names[4]} has {number_of_AB} {object}, and {str(sentences[2])} So, {names[2]} has {number_of_BC} {object}.",
            f"{names[2]} has {number_of_BC} {object}, and {str(sentences[3])} So, {names[3]} has {number_of_CD} {object}.",
            f"The final answer is {number_of_CD}."
        ]
        answer = number_of_CD
        return gold_outputs, answer
    """
    def _make_minimum_tree(self, name1, relate_name:str,object:str="apples",num=random.randint(0,5)) -> List[Sentence]:
        sentences = []
        sentences.append(RelationalSentence(name1,num,relate_name=relate_name,operator=random.choice(["more","less"]),object=object))
        return sentences




def main(args):
    seed=42
    random.seed(seed)
    np.random.seed(seed)
    output_flat_file = Path(args.output_dir) / "flat" / "test.jsonl"
    output_overlap_file = Path(args.output_dir) / "overlap" / "test.jsonl"
    output_negative_file = Path(args.output_dir) / "negative" / "test.jsonl"
    output_position_file = Path(args.output_dir) / "position" / "test.jsonl"
    #output_logic_file = Path(args.output_dir) / "logic" / "test.jsonl"
    
    
    for dir in ["flat","overlap","negative","position"]:
        os.makedirs(Path(args.output_dir) / dir, exist_ok=True)
    with open(Path(output_flat_file),"w") as f_flat, open(output_overlap_file,"w") as f_overlap, open(output_negative_file,"w") as f_negative, open(output_position_file,"w") as f_position:
        for _ in range(300):
            instance = Instance()
            sentences = " ".join([str(s) for s in instance.sentences])
            overlap_sentences = " ".join([str(s) for s in instance.overlap_sentences])
            negative_sentences = " ".join([str(s) for s in instance.negative_sentences])
            position_sentences = " ".join([str(s) for s in instance.position_sentences])
            #logic_sentences = " ".join([str(s) for s in instance.logic_sentences])
            
            for f, sentences in zip([f_flat,f_overlap,f_negative,f_position],[sentences,overlap_sentences,negative_sentences,position_sentences]):
                input = "Context: " + sentences+"\nQuestion: "+instance.question + "\n"
                
                sentence_p = instance.sentence_p if f != f_overlap else instance.sentence_overlap_p
                json_data = {
                    "input": input,
                    "answer": instance.answer,
                    "gold_outputs": instance.gold_outputs,
                    "sentence_p": sentence_p,
                    "redundant_number": instance.redundant_number,
                }
                f.write(json.dumps(json_data))
                f.write('\n')
            """    
            input = "Context: " + logic_sentences+"\nQuestion: "+instance.question + "\n"
            json_data = {
                "input": input,
                "answer": instance.logic_answer,
                "gold_outputs": instance.logic_gold_outputs,
                "sentence_p": instance.sentence_p,
                "redundant_number": instance.redundant_number,
            }
            f_logic.write(json.dumps(json_data))
            f_logic.write('\n')
            """

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--output_dir', default="save/test")
    parser.add_argument('--data_type', default="flat")
    args = parser.parse_args()
    main(args)
