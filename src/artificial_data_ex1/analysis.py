import argparse

from src.artificial_data_ex1.utils import load_jsonl, eval_step, get_answer

def main(args):
    pred_data = load_jsonl(args.pred_file)
    gold_data = load_jsonl(args.gold_file)
    sentence_p_inference = 0
    accuracy = 0
    for pred, gold in zip(pred_data,gold_data):
        pred_output = pred["pred_output"]
        sentence_p = pred["sentence_p"]
        answer = gold["answer"]

        if eval_step(pred_output, sentence_p):
            sentence_p_inference += 1

        pred_answer = get_answer(pred_output)
        print("pred_answer: ", pred_answer)
        print("gold_answer: ", answer)
        if str(answer) == pred_answer:
            accuracy += 1

    print("Percentage of sentence_p inference：", sentence_p_inference/len(pred_data))
    print("Accuracy: ", accuracy/len(pred_data))
    print(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--pred_file', default="test1,valid2")
    parser.add_argument('--gold_file', default="test1,valid2")
    args = parser.parse_args()
    main(args)