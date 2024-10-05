import argparse
import numpy as np
import random
from pathlib import Path
import numpy as np
import os
from typing import List, Dict, Set
import copy
import json

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
    def __init__(self,problem_type="base") -> None:
        self.name_set = {"Alice","Bob","Carol","Dave","Eve","Frank","Grace","Heidi","Ivan","Judy","Kevin","Larry","Mallory","Nancy","Olivia","Peggy","Quentin","Rob","Sybil","Trent","Ursula","Victor","Walter","Xavier","Yvonne","Zoe","Ana","Bill","Cathy","Dan","Ed","Gina","Hank","Ivy","Jack","Kim","Lance","Mia","Nick","Olive","Paul","Quinn","Ruth","Sam","Tina","Vince","Wendy","Zack","Amy","Ben","Cindy","Dylan","Emma","Finn","Aliyah","Alton","Brad","Brande","Callie","Chad","Debbi","Derrek","Emery","Eugene","Franklyn","Heath","Iola","Jake","Jill","Kacey","Kara","Kristopher","Leta","Maleah","Sammy"}
        print(len(self.name_set))
        self.object = random.choice(["apples","bananas","grapes","pencils","books"])
        if "base" == problem_type:
            self.sentences, self.question, self.answer, self.gold_outputs, self.not_gold_outputs = self._make_instance()
        elif "distract" == problem_type:
            self.sentences, self.question, self.answer, self.gold_outputs, self.heuristic_outputs,self.distract_outputs = self._make_instance_distract(child_num=3)
        elif "distract_5" == problem_type:
            self.sentences, self.question, self.answer, self.gold_outputs, self.heuristic_outputs,self.distract_outputs = self._make_instance_distract(child_num=5)
        elif "distract_10" == problem_type:
            self.sentences, self.question, self.answer, self.gold_outputs, self.heuristic_outputs,self.distract_outputs = self._make_instance_distract(child_num=10)
        elif "random" == problem_type:
            init_node = random.randint(1,3)
            child_num = random.randint(2,5)
            random_rate = 0.3
            self.sentences, self.question, self.answer, self.gold_outputs, self.not_gold_outputs = self._make_instance_random(init_node=init_node,depth=5, child_num=child_num,random_rate=random_rate)

    def _get_random_names(self, name_num) -> str:
        try:
            names = random.sample(list(self.name_set), k=name_num)
        except ValueError:
            print("name_num: ", name_num)
            print("name_set: ", self.name_set)
        self.name_set -= set(names)
        return names

    def _get_random_name(self) -> str:
        return self._get_random_names(1)[0]

    def _make_instance_distract(self):
        pass

    def _make_instance_random(self):
        pass

    def _make_outputs(self,gold_sentences:List[Sentence],heuristic_sentences:List[Sentence],distract_sentences:List[Sentence]=None):
        answer = gold_sentences[0].number
        gold_outputs = []
        heuristic_outputs = []
        distract_outputs = []
        child_num = int(len(distract_sentences)/(len(gold_sentences)-1))
        
        first_sentence = str(gold_sentences[0])[:-1]
        for i in range(1, len(gold_sentences)):
            if gold_sentences[i].operator == "more":
                gold_outputs.append(f"{first_sentence}, and {str(gold_sentences[i])} So, {gold_sentences[i].name} has {answer}+{gold_sentences[i].number}={answer+gold_sentences[i].number} {self.object}.")
                answer += gold_sentences[i].number
                first_sentence = f"{gold_sentences[i].name} has {answer} {self.object}"
            elif gold_sentences[i].operator == "fewer":
                gold_outputs.append(f"{first_sentence}, and {str(gold_sentences[i])} So, {gold_sentences[i].name} has {answer}-{gold_sentences[i].number}={answer-gold_sentences[i].number} {self.object}.")
                answer -= gold_sentences[i].number
                first_sentence = f"{gold_sentences[i].name} has {answer} {self.object}"
                
            if heuristic_sentences[i-1].operator == "more":
                heuristic_outputs.append(f"{first_sentence}, and {str(heuristic_sentences[i-1])} So, {heuristic_sentences[i-1].name} has {answer}+{heuristic_sentences[i-1].number}={answer+heuristic_sentences[i-1].number} {self.object}.")
            elif heuristic_sentences[i-1].operator == "fewer":
                heuristic_outputs.append(f"{first_sentence}, and {str(heuristic_sentences[i-1])} So, {heuristic_sentences[i-1].name} has {answer}-{heuristic_sentences[i-1].number}={answer-heuristic_sentences[i-1].number} {self.object}.")
        
            for j in range(child_num):
                if distract_sentences[(i-1)*child_num+j].operator == "more":
                    distract_outputs.append(f"{first_sentence}, and {str(distract_sentences[(i-1)*child_num+j])} So, {distract_sentences[(i-1)*child_num+j].name} has {answer}+{distract_sentences[(i-1)*child_num+j].number}={answer+distract_sentences[(i-1)*child_num+j].number} {self.object}.")
                elif distract_sentences[(i-1)*child_num+j].operator == "fewer":
                    distract_outputs.append(f"{first_sentence}, and {str(distract_sentences[(i-1)*child_num+j])} So, {distract_sentences[(i-1)*child_num+j].name} has {answer}-{distract_sentences[(i-1)*child_num+j].number}={answer-distract_sentences[(i-1)*child_num+j].number} {self.object}.")                        
        return answer, gold_outputs, heuristic_outputs, distract_outputs

    def _make_instance(self, name_num:int=19) -> List[Sentence]:
        names = self._get_random_names(name_num)
        
        
        #0,1,3,7,15
        sentences = []
        sentences.append(Sentence(names[0],random.randint(0,100),object=self.object))
        sentences += self._make_minimum_tree(names[1],names[2],names[0])
        sentences += self._make_minimum_tree(names[3],names[4],names[1])
        sentences += self._make_minimum_tree(names[5],names[6],names[2])
        sentences += self._make_minimum_tree(names[7],names[8],names[3])
        sentences += self._make_minimum_tree(names[9],names[10],names[4])
        sentences += self._make_minimum_tree(names[11],names[12],names[5])
        sentences += self._make_minimum_tree(names[13],names[14],names[6])
        sentences += self._make_minimum_tree(names[15],names[16],names[7])
        sentences += self._make_minimum_tree(names[17],names[18],names[8])
        
        
        question = f"How many {self.object} does {names[15]} have?"
        gold_outputs = []
        
        if sentences[1].operator == "more":
            number_of_AB = sentences[0].number + sentences[1].number
            gold_outputs.append(f"{str(sentences[0])[:-1]}, and {str(sentences[1])} So, {names[1]} has {sentences[0].number}+{sentences[1].number}={number_of_AB} {self.object}.")
        elif sentences[1].operator == "fewer":
            number_of_AB = sentences[0].number - sentences[1].number
            gold_outputs.append(f"{str(sentences[0])[:-1]}, and {str(sentences[1])} So, {names[1]} has {sentences[0].number}-{sentences[1].number}={number_of_AB} {self.object}.")
        
        if sentences[3].operator == "more":
            number_of_BC = number_of_AB + sentences[3].number
            gold_outputs.append(f"{names[1]} has {number_of_AB} {self.object}, and {str(sentences[3])} So, {names[3]} has {number_of_AB}+{sentences[3].number}={number_of_BC} {self.object}.")
        elif sentences[3].operator == "fewer":
            number_of_BC = number_of_AB - sentences[3].number
            gold_outputs.append(f"{names[1]} has {number_of_AB} {self.object}, and {str(sentences[3])} So, {names[3]} has {number_of_AB}-{sentences[3].number}={number_of_BC} {self.object}.")
        if sentences[7].operator == "more":
            number_of_CD = number_of_BC + sentences[7].number
            gold_outputs.append(f"{names[3]} has {number_of_BC} {self.object}, and {str(sentences[7])} So, {names[7]} has {number_of_BC}+{sentences[7].number}={number_of_CD} {self.object}.")
        elif sentences[7].operator == "fewer":
            number_of_CD = number_of_BC - sentences[7].number
            gold_outputs.append(f"{names[3]} has {number_of_BC} {self.object}, and {str(sentences[7])} So, {names[7]} has {number_of_BC}-{sentences[7].number}={number_of_CD} {self.object}.")
        if sentences[15].operator == "more":
            number_of_DE = number_of_CD + sentences[15].number
            gold_outputs.append(f"{names[7]} has {number_of_CD} {self.object}, and {str(sentences[15])} So, {names[15]} has {number_of_CD}+{sentences[15].number}={number_of_DE} {self.object}.")
        elif sentences[15].operator == "fewer":
            number_of_DE = number_of_CD - sentences[15].number
            gold_outputs.append(f"{names[7]} has {number_of_CD} {self.object}, and {str(sentences[15])} So, {names[15]} has {number_of_CD}-{sentences[15].number}={number_of_DE} {self.object}.")
            
        gold_outputs.append(f"The final answer is {number_of_CD}.")
        
        not_gold_outputs = [
            f"{str(sentences[0])[:-1]}, and {str(sentences[2])} So, {names[2]} has x {self.object}.",
            f"{names[1]} has x {self.object}, and {str(sentences[4])} So, {names[4]} has x {self.object}.",
            f"{names[3]} has x {self.object}, and {str(sentences[8])} So, {names[8]} has x {self.object}.",
            f"{names[7]} has x {self.object}, and {str(sentences[16])} So, {names[16]} has x {self.object}."
        ]
        shuffle_sentences = copy.deepcopy(sentences)
        random.shuffle(shuffle_sentences)

        shuffle_sentences = [str(s) for s in shuffle_sentences]
        return shuffle_sentences, question, number_of_CD, gold_outputs, not_gold_outputs
    
    def _make_minimum_tree(self, name1, name2, relate_name:str) -> List[Sentence]:
        sentences = []
        sentences.append(RelationalSentence(name1,random.randint(0,100),relate_name=relate_name,operator=random.choice(["more","fewer"]),object=self.object))
        sentences.append(RelationalSentence(name2,random.randint(0,100),relate_name=relate_name,operator=random.choice(["more","fewer"]),object=self.object))
        return sentences

    def _make_sentences(self,sentence_num:int=1):
        sentences = []
        for _ in range(sentence_num):
            name = self._get_random_name()
            number = random.randint(0,100)
            sentences.append(Sentence(name,number,object=self.object))
        return sentences

    def extend_instance(self,sentences:List[Sentence],node_sentence:Sentence,child_num:int=2):
        child_sentences = []
        for _ in range(child_num):
            name = self._get_random_name()
            number = random.randint(0,100)
            operator = random.choice(["more","fewer"])
            sentence = RelationalSentence(name=name,number=number,relate_name=node_sentence.name,operator=operator,object=self.object)
            child_sentences.append(sentence)

        indexes = sorted(random.sample(range(len(sentences)+child_num),k=child_num))
        for i in indexes:
            sentences.insert(i,child_sentences.pop())

        return sentences, child_sentences

class OverlapInstance(Instance):
    def __init__(self,problem_type="base") -> None:
        self.name_set = {"Alice","Bob","Carol","Dave","Eve","Frank","Grace","Heidi","Ivan","Judy","Kevin","Larry","Mallory","Nancy","Olivia","Peggy","Quentin","Rob","Sybil","Trent","Ursula","Victor","Walter","Xavier","Yvonne","Zoe","Ana","Bill","Cathy","Dan","Ed","Gina","Hank","Ivy","Jack","Kim","Lance","Mia","Nick","Olive","Paul","Quinn","Ruth","Sam","Tina","Vince","Wendy","Zack","Amy","Ben","Cindy","Dylan","Emma","Finn","Gina","Hank","Ivy","Jack","Kim","Lance","Mia","Nick","Olive","Paul","Quinn","Ruth","Sam","Tina","Vince","Wendy","Zack"}
        self.question_name = random.choice(list(self.name_set))
        self.name_set -= {self.question_name}
        self.similar_name = {"'s mother","'s father","'s son","'s neighborhood","'s friend","'s classmate","'s grandparent"}
        self.object = random.choice(["apples","bananas","grapes","pencils","books"])
        
        if problem_type == "base":
            self.sentences, self.question, self.answer, self.gold_outputs, self.not_gold_outputs = self._make_instance()
        elif problem_type == "distract":
            self.sentences, self.question, self.answer, self.gold_outputs, self.heuristic_outputs,self.distract_outputs = self._make_instance_distract(child_num=3)
        elif problem_type == "distract_5":
            self.sentences, self.question, self.answer, self.gold_outputs, self.heuristic_outputs,self.distract_outputs = self._make_instance_distract(child_num=5)
        elif problem_type == "distract_10":
            self.sentences, self.question, self.answer, self.gold_outputs, self.heuristic_outputs,self.distract_outputs = self._make_instance_distract(child_num=10)
        elif problem_type == "random":
            init_node = random.randint(1,3)
            child_num = random.randint(2,5)
            random_rate = 0.3
            self.sentences, self.question, self.answer, self.gold_outputs, self.not_gold_outputs = self._make_instance_random(init_node=init_node,depth=5, child_num=child_num,random_rate=random_rate)

    def get_random_similar_name(self):
        similar_name = random.choice(list(self.similar_name))
        self.similar_name -= {similar_name}
        return similar_name

    def extend_instance_from_gold(self,sentences:List[Sentence],node_sentence:Sentence,child_num:int=3,gold_name:str=None):
        child_sentences = []
        for i in range(child_num):
            if i == 0: 
                name = gold_name
            elif i == 1:
                name = self.question_name+self.get_random_similar_name()
            else:
                name = self._get_random_name()
            number = random.randint(0,100)
            operator = random.choice(["more","fewer"])
            index = random.choice(range(len(sentences)+1))
            sentence = RelationalSentence(name=name,number=number,relate_name=node_sentence.name,operator=operator,object=self.object)
            sentences.insert(index,sentence)
            child_sentences.append(sentence)
        
        assert len(child_sentences) > 2, "child_sentences must be more than 2"
        gold_sentence = child_sentences[0]
        heuristic_sentence = child_sentences[1]
        distract_sentences = child_sentences[2:]
        return sentences, gold_sentence, heuristic_sentence, distract_sentences
    
    
    def _make_instance_distract(self, init_node:int=1,depth:int=5, child_num:int=3) -> List[Sentence]:
        init_sentence = Sentence(name=self._get_random_name(),number=random.randint(0,100),object=self.object)
        gold_sentences=[init_sentence]
        
        heuristic_sentences=[]
        distract_sentences = []
        sentences = [init_sentence]
        node_stack = []
        for _ in range(init_node-1):
            init_sentence = Sentence(name=self._get_random_name(),number=random.randint(0,100),object=self.object)
            node_stack.append((1,init_sentence))

        for tmp_depth in range(1,depth):
            gold_name = self.question_name if tmp_depth == (depth-1) else self._get_random_name()
            sentences, gold_sentence, heuristic_sentence,tmp_distract_sentences = self.extend_instance_from_gold(sentences, gold_sentences[-1],child_num=child_num,gold_name=gold_name)
            gold_sentences.append(gold_sentence)
            heuristic_sentences.append(heuristic_sentence)
            distract_sentences.extend(tmp_distract_sentences)
            node_stack.append((tmp_depth+1,heuristic_sentence))
            #node_stack.append((tmp_depth+1,distract_sentence))
        
        while node_stack:
            tmp_depth,node_sentence = node_stack.pop()
            if tmp_depth < depth:
                sentences, child_sentences = self.extend_instance(sentences, node_sentence,child_num=2) #TODO: child_num=2
                for child_sentence in child_sentences:
                    node_stack.append((tmp_depth+1,child_sentence))
        
        question = f"How many {self.object} does {gold_sentences[-1].name} have?"
        answer, gold_outputs, heuristic_outputs, distract_outputs = self._make_outputs(gold_sentences,heuristic_sentences,distract_sentences)
        
        return sentences, question, answer, gold_outputs, heuristic_outputs, distract_outputs


    def _make_instance_random(self, init_node:int=1,depth:int=5, child_num:int=3,random_rate:float=0.5) -> List[Sentence]:
        init_sentence = Sentence(name=self._get_random_name(),number=random.randint(0,100),object=self.object)
        gold_sentences=[init_sentence]
        
        heuristic_sentences=[]
        distract_sentences = []
        sentences = [init_sentence]
        node_stack = []
        for _ in range(init_node-1):
            init_sentence = Sentence(name=self._get_random_name(),number=random.randint(0,100),object=self.object)
            node_stack.append((1,init_sentence))

        for tmp_depth in range(1,depth):
            gold_name = self.question_name if tmp_depth == depth-1 else self._get_random_name()
            sentences, gold_sentence, heuristic_sentence = self.extend_instance_from_gold(sentences, gold_sentences[-1],child_num=child_num,gold_name=gold_name)
            gold_sentences.append(gold_sentence)
            heuristic_sentences.append(heuristic_sentence)
            if random.random() < random_rate:
                node_stack.append((tmp_depth+1,heuristic_sentence))
        
        while node_stack:
            tmp_depth,node_sentence = node_stack.pop()
            if tmp_depth < depth:
                sentences, child_sentences = self.extend_instance(sentences, node_sentence,child_num=child_num-1)
                for child_sentence in child_sentences:
                    if random.random() < random_rate:
                        node_stack.append((tmp_depth+1,child_sentence))
        
        question = f"How many {self.object} does {gold_sentences[-1].name} have?"
        answer, gold_outputs, heuristic_outputs,distract_outputs = self._make_outputs(gold_sentences,heuristic_sentences,distract_sentences)
        
        return sentences, question, answer, gold_outputs, heuristic_outputs, distract_outputs

    def _make_instance(self, name_num:int=19) -> List[Sentence]:
        names = self._get_random_names(name_num)
        name2 = self.question_name + self.similar_name.pop()
        name4 = self.question_name + self.similar_name.pop()
        name8 = self.question_name + self.similar_name.pop()
        #name8 = self.question_name + self.similar_name.pop()
        
        
        #0,1,3,7,15
        sentences = []
        sentences.append(Sentence(names[0],random.randint(0,5),object=self.object))
        sentences += self._make_minimum_tree(names[1],name2,names[0])
        sentences += self._make_minimum_tree(names[3],name4,names[1])
        sentences += self._make_minimum_tree(names[5],names[6],name2)
        sentences += self._make_minimum_tree(names[7],name8,names[3])
        sentences += self._make_minimum_tree(names[9],names[10],name4)
        sentences += self._make_minimum_tree(names[11],names[12],names[5])
        sentences += self._make_minimum_tree(names[13],names[14],names[6])
        sentences += self._make_minimum_tree(self.question_name,names[16],names[7])
        sentences += self._make_minimum_tree(names[17],names[18],name8)
        
        
        question = f"How many {self.object} does {self.question_name} have?"
        
        gold_outputs = []
        
        if sentences[1].operator == "more":
            number_of_AB = sentences[0].number + sentences[1].number
            gold_outputs.append(f"{str(sentences[0])[:-1]}, and {str(sentences[1])} So, {names[1]} has {sentences[0].number}+{sentences[1].number}={number_of_AB} {self.object}.")
        elif sentences[1].operator == "fewer":
            number_of_AB = sentences[0].number - sentences[1].number
            gold_outputs.append(f"{str(sentences[0])[:-1]}, and {str(sentences[1])} So, {names[1]} has {sentences[0].number}-{sentences[1].number}={number_of_AB} {self.object}.")
        
        if sentences[3].operator == "more":
            number_of_BC = number_of_AB + sentences[3].number
            gold_outputs.append(f"{names[1]} has {number_of_AB} {self.object}, and {str(sentences[3])} So, {names[3]} has {number_of_AB}+{sentences[3].number}={number_of_BC} {self.object}.")
        elif sentences[3].operator == "fewer":
            number_of_BC = number_of_AB - sentences[3].number
            gold_outputs.append(f"{names[1]} has {number_of_AB} {self.object}, and {str(sentences[3])} So, {names[3]} has {number_of_AB}-{sentences[3].number}={number_of_BC} {self.object}.")
            
        if sentences[7].operator == "more":
            number_of_CD = number_of_BC + sentences[7].number
            gold_outputs.append(f"{names[3]} has {number_of_BC} {self.object}, and {str(sentences[7])} So, {names[7]} has {number_of_BC}+{sentences[7].number}={number_of_CD} {self.object}.")
        elif sentences[7].operator == "fewer":
            number_of_CD = number_of_BC - sentences[7].number
            gold_outputs.append(f"{names[3]} has {number_of_BC} {self.object}, and {str(sentences[7])} So, {names[7]} has {number_of_BC}-{sentences[7].number}={number_of_CD} {self.object}.")
        if sentences[15].operator == "more":
            number_of_DE = number_of_CD + sentences[15].number
            gold_outputs.append(f"{names[7]} has {number_of_CD} {self.object}, and {str(sentences[15])} So, {self.question_name} has {number_of_CD}+{sentences[15].number}={number_of_DE} {self.object}.")
        elif sentences[15].operator == "fewer":
            number_of_DE = number_of_CD - sentences[15].number
            gold_outputs.append(f"{names[7]} has {number_of_CD} {self.object}, and {str(sentences[15])} So, {self.question_name} has {number_of_CD}-{sentences[15].number}={number_of_DE} {self.object}.")
        
        
        gold_outputs.append(f"The final answer is {number_of_DE}.")
        not_gold_outputs = [
            f"{str(sentences[0])[:-1]}, and {str(sentences[2])} So, {name2} has x {self.object}.",
            f"{names[1]} has x {self.object}, and {str(sentences[4])} So, {name4} has x {self.object}.",
            f"{names[3]} has x {self.object}, and {str(sentences[8])} So, {name8} has x {self.object}.",
        ]
        shuffle_sentences = copy.deepcopy(sentences)
        random.shuffle(shuffle_sentences)
        shuffle_sentences = [str(s) for s in shuffle_sentences]
        return shuffle_sentences, question, number_of_DE, gold_outputs, not_gold_outputs




    
class NegativeInstance(Instance):
    def _make_minimum_tree(self, name1, name2, relate_name:str) -> List[Sentence]:
        sentences = []
        sentences.append(RelationalSentence(name1,random.randint(0,5),relate_name=relate_name,operator=random.choice(["more","fewer"]),object=self.object, negative="has"))
        sentences.append(RelationalSentence(name2,random.randint(0,5),relate_name=relate_name,operator=random.choice(["more","fewer"]),object=self.object, negative="doesn't have"))
        return sentences

class PositionalInstance(Instance):

    def extend_instance_from_gold(self,sentences:List[Sentence],node_sentence:Sentence,child_num:int=3):
        child_sentences = []
        distract_sentences = []
        for _ in range(child_num):
            name = self._get_random_name()
            number = random.randint(0,100)
            operator = random.choice(["more","fewer"])
            child_sentences.append(RelationalSentence(name=name,number=number,relate_name=node_sentence.name,operator=operator,object=self.object))
        
        indexes = sorted(random.sample(range(len(sentences)+child_num),k=child_num))
        gold_index = random.choice(indexes[1:])
        
        for i in indexes:
            sentences.insert(i,child_sentences.pop())
        gold_sentence = sentences[gold_index]
        heuristic_sentence = sentences[indexes[0]]
        indexes.remove(gold_index)
        _ = indexes.pop(0)
        distract_sentences = [sentences[i] for i in indexes]
        return sentences, gold_sentence, heuristic_sentence,distract_sentences


    
    def _make_instance_distract(self, init_node:int=1,depth:int=5,child_num:int=3) -> List[Sentence]:
        init_sentence = Sentence(name=self._get_random_name(),number=random.randint(0,100),object=self.object)
        gold_sentences=[init_sentence]
        
        heuristic_sentences=[]
        distract_sentences = []
        sentences = [init_sentence]
        node_stack = []
        for _ in range(init_node-1):
            init_sentence = Sentence(name=self._get_random_name(),number=random.randint(0,100),object=self.object)
            node_stack.append((1,init_sentence))

        for tmp_depth in range(1,depth):
            sentences, gold_sentence, heuristic_sentence,tmp_distract_sentences = self.extend_instance_from_gold(sentences, gold_sentences[-1],child_num=child_num)
            gold_sentences.append(gold_sentence)
            heuristic_sentences.append(heuristic_sentence)
            distract_sentences.extend(tmp_distract_sentences)
            node_stack.append((tmp_depth+1,heuristic_sentence))
        
        while node_stack:
            tmp_depth,node_sentence = node_stack.pop()
            if tmp_depth < depth:
                sentences, child_sentences = self.extend_instance(sentences, node_sentence,child_num=2) #TODO: child_num=2
                for child_sentence in child_sentences:
                    node_stack.append((tmp_depth+1,child_sentence))
        
        question = f"How many {self.object} does {gold_sentences[-1].name} have?"
        answer, gold_outputs, heuristic_outputs, distract_outputs = self._make_outputs(gold_sentences,heuristic_sentences,distract_sentences)
        
        return sentences, question, answer, gold_outputs, heuristic_outputs, distract_outputs
        
        
    def _make_instance_random(self, init_node:int=1,depth:int=5,child_num:int=3,random_rate:float=0.5) -> List[Sentence]:
        init_sentence = Sentence(name=self._get_random_name(),number=random.randint(0,100),object=self.object)
        gold_sentences=[init_sentence]
        
        heuristic_sentences=[]
        sentences = [init_sentence]
        node_stack = []
        for _ in range(init_node-1):
            init_sentence = Sentence(name=self._get_random_name(),number=random.randint(0,100),object=self.object)
            if random.random() < random_rate:
                node_stack.append((1,init_sentence))

        for tmp_depth in range(1,depth):
            sentences, gold_sentence, heuristic_sentence = self.extend_instance_from_gold(sentences, gold_sentences[-1],child_num=child_num)
            gold_sentences.append(gold_sentence)
            heuristic_sentences.append(heuristic_sentence)
            node_stack.append((tmp_depth+1,heuristic_sentence))
        
        while node_stack:
            tmp_depth,node_sentence = node_stack.pop()
            if tmp_depth < depth:
                sentences, child_sentences = self.extend_instance(sentences, node_sentence,child_num=child_num-1)
                for child_sentence in child_sentences:
                    if random.random() < random_rate:
                        node_stack.append((tmp_depth+1,child_sentence))
        
        question = f"How many {self.object} does {gold_sentences[-1].name} have?"
        answer, gold_outputs, not_gold_outputs = self._make_outputs(gold_sentences,heuristic_sentences)
        
        return sentences, question, answer, gold_outputs, not_gold_outputs
    
    def _make_instance(self, name_num:int=19) -> List[Sentence]:
        names = self._get_random_names(name_num)
        
        #0,1,3,7,15
        sentences = []
        sentences.append(Sentence(names[0],random.randint(0,5),object=self.object))
        sentences += self._make_minimum_tree(names[5],names[6],names[2],)
        sentences += self._make_minimum_tree(names[9],names[10],names[4])
        sentences += self._make_minimum_tree(names[11],names[12],names[5])
        sentences += self._make_minimum_tree(names[13],names[14],names[6])
        sentences += self._make_minimum_tree(names[17],names[18],names[8])
        shuffle_sentences = copy.deepcopy(sentences)
        
        random.shuffle(shuffle_sentences)
        sentence1 = self._make_minimum_tree(names[1],names[2],names[0])
        i0,i1 = sorted(random.sample(range(len(shuffle_sentences)+2),k=2))
        shuffle_sentences.insert(i0,sentence1[1])
        shuffle_sentences.insert(i1,sentence1[0])
        sentence2 = self._make_minimum_tree(names[3],names[4],names[1])
        i0,i1 = sorted(random.sample(range(len(shuffle_sentences)+2),k=2))
        shuffle_sentences.insert(i0,sentence2[1])
        shuffle_sentences.insert(i1,sentence2[0])
        sentence3 = self._make_minimum_tree(names[7],names[8],names[3])
        i0,i1 = sorted(random.sample(range(len(shuffle_sentences)+2),k=2))
        shuffle_sentences.insert(i0,sentence3[1])
        shuffle_sentences.insert(i1,sentence3[0])
        sentence4 = self._make_minimum_tree(names[15],names[16],names[7])
        i0,i1 = sorted(random.sample(range(len(shuffle_sentences)+2),k=2))
        shuffle_sentences.insert(i0,sentence4[1])
        shuffle_sentences.insert(i1,sentence4[0])
        
        
        gold_outputs = []
        question = f"How many {self.object} does {names[15]} have?"
        if sentence1[0].operator == "more":
            number_of_AB = sentences[0].number + sentence1[0].number
            gold_outputs.append(f"{str(sentences[0])[:-1]}, and {str(sentence1[0])} So, {names[1]} has {sentences[0].number}+{sentence1[0].number}={number_of_AB} {self.object}.")
        elif sentence1[0].operator == "fewer":
            number_of_AB = sentences[0].number - sentence1[0].number
            gold_outputs.append(f"{str(sentences[0])[:-1]}, and {str(sentence1[0])} So, {names[1]} has {sentences[0].number}-{sentence1[0].number}={number_of_AB} {self.object}.")
        
        if sentence2[0].operator == "more":
            number_of_BC = number_of_AB + sentence2[0].number
            gold_outputs.append(f"{names[1]} has {number_of_AB} {self.object}, and {str(sentence2[0])} So, {names[3]} has {number_of_AB}+{sentence2[0].number}={number_of_BC} {self.object}.")
        elif sentence2[0].operator == "fewer":
            number_of_BC = number_of_AB - sentence2[0].number
            gold_outputs.append(f"{names[1]} has {number_of_AB} {self.object}, and {str(sentence2[0])} So, {names[3]} has {number_of_AB}-{sentence2[0].number}={number_of_BC} {self.object}.")
            
        if sentence3[0].operator == "more":
            number_of_CD = number_of_BC + sentence3[0].number
            gold_outputs.append(f"{names[3]} has {number_of_BC} {self.object}, and {str(sentence3[0])} So, {names[7]} has {number_of_BC}+{sentence3[0].number}={number_of_CD} {self.object}.")
        elif sentence3[0].operator == "fewer":
            number_of_CD = number_of_BC - sentence3[0].number
            gold_outputs.append(f"{names[3]} has {number_of_BC} {self.object}, and {str(sentence3[0])} So, {names[7]} has {number_of_BC}-{sentence3[0].number}={number_of_CD} {self.object}.")
        if sentence4[0].operator == "more":
            number_of_DE = number_of_CD + sentence4[0].number
            gold_outputs.append(f"{names[7]} has {number_of_CD} {self.object}, and {str(sentence4[0])} So, {names[15]} has {number_of_CD}+{sentence4[0].number}={number_of_DE} {self.object}.")
        elif sentence4[0].operator == "fewer":
            number_of_DE = number_of_CD - sentence4[0].number
            gold_outputs.append(f"{names[7]} has {number_of_CD} {self.object}, and {str(sentence4[0])} So, {names[15]} has {number_of_CD}-{sentence4[0].number}={number_of_DE} {self.object}.")
        
        gold_outputs.append(f"The final answer is {number_of_DE}.")
        not_gold_outputs = [
            f"{str(sentences[0])[:-1]}, and {str(sentence1[1])} So, {names[2]} has x {self.object}.",
            f"{names[1]} has x {self.object}, and {str(sentence2[1])} So, {names[4]} has x {self.object}.",
            f"{names[3]} has x {self.object}, and {str(sentence3[1])} So, {names[8]} has x {self.object}.",
            f"{names[7]} has x {self.object}, and {str(sentence4[1])} So, {names[16]} has x {self.object}."
        ]

        shuffle_sentences = [str(s) for s in shuffle_sentences]
        return shuffle_sentences, question, number_of_DE, gold_outputs, not_gold_outputs



def main(args):
    seed=44
    random.seed(seed)
    np.random.seed(seed)
    
    os.makedirs(Path(args.output_file).parent, exist_ok=True)
    with open(Path(args.output_file),"w") as f:
        for _ in range(100): #300
            if args.data_type == "overlap":
                instance = OverlapInstance(problem_type="base")
            elif args.data_type == "negative":
                instance = NegativeInstance()
            elif args.data_type == "position":
                instance = PositionalInstance(problem_type="base")
            elif args.data_type == "overlap_distract":
                instance = OverlapInstance(problem_type="distract")
            elif args.data_type == "position_distract":
                instance = PositionalInstance(problem_type="distract")
            elif args.data_type == "overlap_distract_5":
                instance = OverlapInstance(problem_type="distract_5")
            elif args.data_type == "position_distract_5":
                instance = PositionalInstance(problem_type="distract_5")
            elif args.data_type == "overlap_distract_10":
                instance = OverlapInstance(problem_type="distract_10")
            elif args.data_type == "position_distract_10":
                instance = PositionalInstance(problem_type="distract_10")
            elif args.data_type == "overlap_random":
                instance = OverlapInstance(problem_type="random")
            elif args.data_type == "position_random":
                instance = PositionalInstance(problem_type="random")
            else:
                print("Unknown data type")
                exit()
            sentences = " ".join([str(s) for s in instance.sentences])

            input = "Context: " + sentences+"\nQuestion: "+instance.question + "\n"
            
            json_data = {
                "input": input,
                "answer": instance.answer,
                "gold_outputs": instance.gold_outputs,
                "heuristic_outputs": instance.heuristic_outputs,
                "distract_outputs": instance.distract_outputs
            }
            f.write(json.dumps(json_data))
            f.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--output_file', default="save/test")
    parser.add_argument('--data_type', default="flat")
    args = parser.parse_args()
    main(args)
