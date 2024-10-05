from pathlib import Path
import re
import json



def read_jsonl_file(input_file: Path):
    inputs = []
    outputs = []
    answers = []
    sentence_ps = []
    number_ps = []
    
    with open(input_file, 'r') as input_json_file:
        for json_data in input_json_file:
            if json_data != "\n":
                json_data = json.loads(json_data)
                inputs.append(json_data["input"])
                outputs.append(json_data["gold_outputs"])
                answers.append(json_data["answer"])
                sentence_ps.append(json_data["sentence_p"])
                number_ps.append(json_data["redundant_number"])
                
    return (inputs,outputs,answers,sentence_ps,number_ps)


def load_jsonl(file_path):
    log_data = []
    with open(file_path, 'r') as input_json_file:
        for json_data in input_json_file:
            if json != "\n":
                log_data.append(json.loads(json_data))
    return log_data


def eval_number_step(pred, number_p):
    try:
        number_regex = re.compile(r"\d+")
        
        pred = re.sub(r"\n", " ", pred)
        numbers = re.findall(number_regex, pred)

        if str(number_p) in numbers:
            print("number_p: ", number_p)
            print("pred: ", pred)
            print("----------------")
            return True
        else:
            return False
    except:
        return False
    
    
def eval_step(pred, sentence_p):
    try:
        sentence_p = re.search(r"(.+?) has", sentence_p).group(1)
        pred = re.sub(r"\n", " ", pred)
        
        pred = re.sub(r"Context.+", "", pred)
        if sentence_p in pred:
            return True
        else:
            return False
    except:
        return False

def get_answer(output:str):
    print(output)
    try:
        output = re.sub(r"\n", "", output)
        regex = re.compile(r"answer is (.+?)\.")
        answer = re.search(regex, output).group(1)
        return answer
    except:
        try: 
            regex = re.compile(r"Therefore.+?has (.+?) ")
            answer = re.search(regex, output).group(1)
            return answer
        except:
            return None

if __name__ == '__main__':
    pred_steps = " Eve is not witty. If Eve is not witty, then Eve is kind. Eve is kind. If Eve is kind, then Eve is honest. Eve is honest. The final answer is False.".split(". ")
    pred_steps = [x.strip() for x in pred_steps]
    gold_steps = "Eve is not witty. If Eve is not witty, then Eve is kind. Eve is kind. If Eve is kind, then Eve is honest. Eve is honest. The final answer is False.".split(". ")
    gold_steps = [x.strip() for x in gold_steps]