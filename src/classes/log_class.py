import torch
from torch.utils.data import Dataset
import numpy as np
from typing import List, Dict, Set,Tuple
import copy
import os
import json


class Log():
    def __init__(self,input,output,final_answer,correct):
        self.input = input
        self.output = output
        self.final_answer = final_answer
        self.correct = correct
    
    def to_dict(self):
        return {
            "input":self.input,
            "output":self.output,
            "final_answer":self.final_answer,
            "correct":self.correct
        }

class LogProcessor():
    def __init__(self, logs: List[Log]=None):
        self.logs = logs
    
    def write(self,output_file_path:str):
        with open(output_file_path, "w") as f:
            for log in self.logs:
                f.write(json.dumps(log.to_dict())+"\n")
    
    def read(self,input_file_path:str):
        logs = []
        with open(input_file_path, "r") as f:
            for line in f:
                log_dict = json.loads(line)
                log = Log(**log_dict)
                logs.append(log)
        self.logs = logs

    def check_output(self):
        correct_num = 0
        for log in self.logs:
            response = log.output
            try: 
                pred_answer = response.split("Final answer is ")[1]
                pred_answer = pred_answer.replace(",","")
                if pred_answer[-1] == ".": pred_answer = pred_answer[:-1]
                
                if pred_answer == log.final_answer:
                    log.correct = True
                else:
                    log.correct = False
            except:
                log.correct = False
            
        print(correct_num/len(self.logs))