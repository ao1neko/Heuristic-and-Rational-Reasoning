from pathlib import Path
import re
import json



def read_jsonl_file(input_file: Path):
    inputs = []
    outputs = []
    answers = []
    
    with open(input_file, 'r') as input_json_file:
        for json_data in input_json_file:
            if json_data != "\n":
                json_data = json.loads(json_data)
                inputs.append(json_data["input"])
                outputs.append(json_data["gold_outputs"])
                answers.append(json_data["answer"])
    return (inputs,outputs,answers)


def load_jsonl(file_path):
    log_data = []
    with open(file_path, 'r') as input_json_file:
        for json_data in input_json_file:
            if json != "\n":
                log_data.append(json.loads(json_data))
    return log_data

def eval_step(pred, gold):
    try: 
        pred = re.sub(r"\n", " ", pred)
        pred = re.sub(r"so", "So", pred)
        pred = re.sub(r",", "", pred)
        pred = re.sub(r"Therefore", "So", pred)
        pred = re.sub(r"Context.+", "", pred)
        
        gold = re.sub(r",", "", gold)
        
        regex = re.compile(r"So (.+?) has")
        gold = re.search(regex, gold).group(1)
        pred = re.search(regex, pred).group(1)
        if gold == pred:
            return True
        else:
            return False
    except:
        return False


def get_answer(output:str):
    try:
        output = re.sub(r"\n", "", output)
        regex = re.compile(r"answer is (.+?).")
        answer = re.search(regex, output).group(1)
        return answer
    except:
        return None

if __name__ == '__main__':
    pred_steps = " Eve is not witty. If Eve is not witty, then Eve is kind. Eve is kind. If Eve is kind, then Eve is honest. Eve is honest. The final answer is False.".split(". ")
    pred_steps = [x.strip() for x in pred_steps]
    gold_steps = "Eve is not witty. If Eve is not witty, then Eve is kind. Eve is kind. If Eve is kind, then Eve is honest. Eve is honest. The final answer is False.".split(". ")
    gold_steps = [x.strip() for x in gold_steps]
    print(eval_answer_and_steps(pred_steps, gold_steps, True, True))