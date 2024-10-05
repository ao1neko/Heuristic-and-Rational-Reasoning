from pathlib import Path
import os
from typing import List, Dict, Set, Tuple
import copy
import json
import os
import openai
import uuid
import re
import math
import random




class GSM8KRedundantData():
    def __init__(self,context:str=None,question:str=None, answer:str=None,reasoning_step:str=None):
        self.context = context
        self.context_names = None
        self.context_numbers = None
        self.question = question
        self.answer = answer
        self.reasoning_step = reasoning_step
        
        self.redundant_sentences = None
        self.redundant_numbers = None

class GSM8KRedundantDataProcessor():
    def __init__(self,data_list:List[GSM8KRedundantData]=None,data_type:str="overlap"):
        self.data_list = data_list
        #self.names = ["Bella","James","Natalia","Carolyn","Artemis","Caleb","Arnel","Gerald","Rachel","Sara","Anna","Ann","Tommy","Sanchez","Lisa","Samantha","Dale","Cate","Bill","Snyder","Mark","Brennan","Randy","Jasper","Albert","Ken","Alexis","Tim","Tobias","Joy","Mary","Ralph","Jack","Noah","Weng","Betty","Julie","Tina","Sam","Gomer","Marty","Ellen","Lorie","Ada","Alani","Anakin","Locsin","John","Mason","Cecilia"]
        self.names = ["Bella","James","Natalia","Carolyn","Artemis","Caleb","Arnel","Gerald","Rachel","Sara","Anna","Ann","Tommy","Sanchez","Lisa","Samantha","Dale","Cate","Bill","Snyder","Mark","Brennan","Randy","Jasper","Albert","Ken","Alexis","Tim","Tobias","Joy","Mary","Ralph","Jack","Noah","Weng","Betty","Julie","Tina","Sam","Gomer","Marty","Ellen","Lorie"]
        self.similar_name = ["'s mother","'s father","'s son","'s neighborhood"]
        self.name_regex = re.compile("|".join(self.names))
        self.pronoun_regex = re.compile(r'\sshe|\shim|\sher|\she|\sShe|\sHim|\sHer|\sHe')
        self.number_regex = re.compile(r'\d+')
        self.tool_regex = re.compile(r'<<(.+?)=.+?>>')
        self.data_type = data_type

    def read_original_file(self, input_file_path: Path):
        with open(input_file_path, 'r') as input_file_object:
            data_list = []
            separate_context_question_regex = re.compile(r'(.+\.)\s(.+?[\?|\.])')
            for json_data in input_file_object:
                try:
                    json_data = json.loads(json_data)
                    separated_question = re.search(
                        separate_context_question_regex, json_data["question"])
                    
                    context = separated_question.group(1)
                    question = separated_question.group(2)
                    
                    reasoning_step = json_data["answer"]
                    separated_answer = reasoning_step.split("\n")
                    answer = separated_answer[-1][5:]

                    if json_data != "\n" :
                        data_instance = GSM8KRedundantData(context=context,question=question,answer=answer,reasoning_step=reasoning_step)
                        data_list.append(data_instance)
                except:
                    print("context: ",context)
            self.data_list = data_list

    def get_redundant_sentences(self):
        for data in self.data_list:
            redundant_sentences = []
            for sentence in data.context[:-1].split(". "):
                if re.search(self.number_regex,sentence) is not None and (re.search(self.name_regex,sentence) is not None or re.search(self.pronoun_regex,sentence) is not None):
                    redundant_sentences.append(sentence)
            data.redundant_sentences = redundant_sentences
    
    def get_context_names(self):
        for data in self.data_list:
            context_names = re.findall(self.name_regex,data.context)
            data.context_names = context_names
    
    def get_context_numbers(self):
        for data in self.data_list:
            context_numbers = list(set(re.findall(self.number_regex,data.reasoning_step)))
            data.context_numbers = context_numbers

    def filter_non_redundant_data(self):
        data_list = []
        for data in self.data_list:
            question_names = re.findall(self.name_regex,data.question)
            question_pronouns = re.findall(self.pronoun_regex,data.question)
            
            if len(data.redundant_sentences) != 0 and len(data.context_names) == 1 and len(question_names + question_pronouns) != 0:
                data_list.append(data)
        self.data_list = data_list

    def replace_context(self):
        for data in self.data_list:
            context = data.context
            context = re.sub(self.pronoun_regex,f" {data.context_names[0]}",context)
            data.context = context

    def replace_question(self):
        for data in self.data_list:
            question = data.question
            question = re.sub(self.pronoun_regex,f" {data.context_names[0]}",question)
            data.question = question

    def _replace_name_redundant_sentences(self,redundant_sentences,replace_names):
        sentences = []
        for sentence in redundant_sentences:
            for replace_name in replace_names:
                tmp_sentence = re.sub(self.name_regex,replace_name,sentence)
                tmp_sentence = re.sub(self.pronoun_regex,f" {replace_name}",tmp_sentence)
                sentences.append(tmp_sentence)
        return sentences

    def _replace_number_redundant_sentences(self,redundant_sentences,replace_numbers):
        sentences = []
        for sentence in redundant_sentences:
            sentence_numbers = re.findall(self.number_regex,sentence)
            for sentence_number in sentence_numbers:
                replace_number = random.choice(replace_numbers)
                sentence = re.sub(sentence_number,replace_number,sentence)
            sentences.append(sentence)
        return sentences


    def add_redundant_sentences_to_context(self,redundant_context_num:int=3):
        data_list = []
        for data in self.data_list:
            other_numbers = [math.floor(int(x)*y) for x in data.context_numbers for y in [0.5,0.8,1.2,1.5,2]]
            other_numbers = [str(x) for x in other_numbers if x not in data.context_numbers]
            
            if self.data_type == "overlap":
                other_names = [data.context_names[0]+x for x in self.similar_name]
            else:
                other_names = list(set(self.names)|set(data.context_names))
                
            if self.data_type == "negative":
                object = random.choice(["apples","bananas","grapes","pencils","books"])
                other_number = other_numbers.pop()
                other_name = other_names.pop()
                redundant_sentences = [f"{other_name} doesn't have {other_number} {object}"]
            elif self.data_type == "not_negative":
                other_number = other_numbers.pop()
                other_name = other_names.pop()
                object = random.choice(["apples","bananas","grapes","pencils","books"])
                redundant_sentences = [f"{other_name} has {other_number} {object}"]
            else:
                redundant_sentences = data.redundant_sentences
                
            redundant_sentences = self._replace_name_redundant_sentences(redundant_sentences,other_names)
            redundant_sentences = self._replace_number_redundant_sentences(redundant_sentences,other_numbers)
            redundant_sentences = random.sample(redundant_sentences, redundant_context_num)
            
            redundant_numbers = list(set(re.findall(self.number_regex," ".join(redundant_sentences))))
            data.redundant_numbers = redundant_numbers
            
            
            tmp_contexts = data.context.split(". ")
            position_index = random.randint(0,len(tmp_contexts))
            not_position_index = random.randint(position_index,len(tmp_contexts)+1)
            if self.data_type == "position":
                tmp_contexts.insert(position_index,". ".join(redundant_sentences))
            else:
                tmp_contexts.insert(not_position_index,". ".join(redundant_sentences))
            data.context =  ". ".join(tmp_contexts)
            data_list.append(data)
        self.data_list = data_list


    def make_instance(self,redundant_context_num:int=3):
        self.get_redundant_sentences()
        self.get_context_names()
        self.get_context_numbers()
        self.filter_non_redundant_data()
        
        self.replace_question()
        self.replace_context()
        
        self.add_redundant_sentences_to_context(redundant_context_num=redundant_context_num)


    def write_file(self, output_file_path: Path):
        os.makedirs(output_file_path, exist_ok=True)
        
        with open(output_file_path, 'w') as output_file_object:
            for data_instance in self.data_list:
                context = data_instance.context
                redundant_numbers = data_instance.redundant_numbers
                json_data={
                    "input": "Context: " + context + "\nQuestion: " + data_instance.question,
                    "answer": data_instance.answer,
                    "redundant_numbers": redundant_numbers,}
                output_file_object.write(
                    json.dumps((json_data)))
                output_file_object.write("\n")