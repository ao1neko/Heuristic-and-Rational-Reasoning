# Software for the paper
The code of [First Heuristic Then Rational: Dynamic Use of Heuristics in Language Model Reasoning](https://arxiv.org/abs/2406.16078).

## Dependencies
Install pytorch-cuda appropriate for each CUDA environment
```
conda create -n search_capability [appropriate pytorch-cuda](https://pytorch.org/get-started/locally/)

# example
conda create -n search_capability pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.6 -c pytorch -c nvidia
```
Install other libraries
```
source activate search_capability
conda install -c conda-forge wandb tqdm openai sentencepiece tenacity
conda install -c huggingface transformers
```


## Make Data
Use dataset GSM8K created in Training Verifiers to Solve Math Word Problems.
Firstly，place GSM8K [test.jsonl](https://github.com/openai/grade-school-math/blob/master/grade_school_math/data/test.jsonl) under data/GSM8K.
Create a dataset to be used for the experiment by running the following.
```
cd scripts/data
./GSM8K_ex1/make_data.sh [project_dir_path]
./artificial_data_ex1/make_data.sh [project_dir_path]
./artificial_data_ex2/make_data.sh [project_dir_path]
```




## Experiment 1 
To use the APIs provided by OpenAI and google, set each api key in the environment variables OPENAI_API_KEY and GOOGLE_API_KEY.
Reproduce experiment 1 by executing the following. 
#### GPT-3.5-turbo, GPT-4
```
# GSM8K Reasoning
./scripts/model/GSM8K_ex1/main.sh [project_dir_path] [heuristic_type] [model_name]

# Artificial Data Reasoning
./scripts/model/artificial_data_ex1/main.sh [project_dir_path] [heuristic_type] flat [model_name]
```
- log is saved at `[project_dir_path]/logs/artificial_data_ex1/[heuristic_type]/flat/[model_name]`
- heuristic_type is flat,overlap,position or negative

example
```
./scripts/model/GSM8K_ex1/main.sh [project_dir_path] overlap gpt-3.5-turbo
```
#### PaLM2
```
# GSM8K Reasoning
./scripts/model/GSM8K_ex1/main_palm2.sh [project_dir_path] [heuristic_type] PaLM2

# Artificial Data Reasoning
./scripts/model/artificial_data_ex1/main_palm2.sh [project_dir_path] [heuristic_type] flat PaLM2
```

#### Llama-2
```
# GSM8K Reasoning
./scripts/model/GSM8K_ex1/main.sh [project_dir_path] [heuristic_type] [model_name]

# Artificial Data Reasoning
./scripts/model/artificial_data_ex1/main.sh [project_dir_path] [heuristic_type] flat [model_name]
```

#### Analysis
```
./scripts/model/GSM8K_ex1/analysis.sh [project_dir_path] [heuristic_type] [model_name]
./scripts/model/artificial_data_ex1/analysis.sh [project_dir_path] [heuristic_type] [model_name]
```


## Experiment 2 
Reproduce experiment 2 by executing the following. 
#### GPT-3.5-turbo, GPT-4
```
./scripts/model/artificial_data_ex2/main.sh [project_dir_path] [heuristic_type] flat [model_name] [reasoning_step]
```
- reasoning_step is 0,1 or 2


#### PaLM2
```
./scripts/model/artificial_data_ex2/main_palm2.sh [project_dir_path] [heuristic_type] flat PaLM2 [reasoning_step]
```

#### Llama-2
```
./scripts/model/artificial_data_ex2/main.sh [project_dir_path] [heuristic_type] flat [model_name] [reasoning_step]
```

#### Analysis
```
./scripts/model/artificial_data_ex2/analysis.sh [project_dir_path] [heuristic_type] [model_name] [reasoning_step]
```