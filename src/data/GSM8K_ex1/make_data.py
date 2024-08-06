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
from pathlib import Path

from src.classes.data_processor_class import  GSM8KRedundantDataProcessor

def main(args):
    seed=42
    random.seed(seed)
    np.random.seed(seed)
    output_dir = Path(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    data_processor = GSM8KRedundantDataProcessor(data_type=args.data_type)
    data_processor.read_original_file(args.input_file)
    data_processor.make_instance(redundant_context_num=1)
    
    output_file = output_dir / f"{args.data_type}.jsonl"
    data_processor.write_file(output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--input_file', default="save/test")
    parser.add_argument('--output_dir', default="save/test")
    parser.add_argument('--data_type', default="overlap")
    args = parser.parse_args()
    main(args)
