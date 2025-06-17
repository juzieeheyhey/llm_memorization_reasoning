import sys, os
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)


import yaml
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.trainer import Trainer
from transformers.training_args import TrainingArguments
from utils.helpers import load_dataset, format_cot_example

cfg = yaml.safe_load(open('config/config.yaml'))

def main():
    tokenizer = AutoTokenizer.from_pretrained(cfg['model_name'])
    model = AutoModelForCausalLM.from_pretrained(cfg['model_name'])
    data = load_dataset('data/processed/train_cot.json')
    examples = [format_cot_example(ex, tokenizer) for ex in data]
    args = TrainingArguments(
        output_dir='models/llama_finetune/cot',
        **cfg['training_args']
    )
    trainer = Trainer(model=model, args=args, train_dataset=examples)
    trainer.train()
    model.save_pretrained(args.output_dir)

if __name__=='__main__': 
    main()