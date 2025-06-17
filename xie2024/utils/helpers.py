import json
from transformers.tokenization_utils import PreTrainedTokenizer

def load_dataset(path: str):
    return json.load(open(path))

def format_qa_example(ex: dict, tokenizer: PreTrainedTokenizer):
    text = '\n'.join(ex['question']) + '\nAnswer:'
    enc = tokenizer(text, return_tensors='pt', truncation=True)
    enc['labels'] = tokenizer(str(ex['answer']), return_tensors='pt').input_ids
    return enc

def format_cot_example(ex: dict, tokenizer: PreTrainedTokenizer):
    text = '\n'.join(ex['question'] + ex.get('reasoning', [])) + '\nAnswer:'
    enc = tokenizer(text, return_tensors='pt', truncation=True)
    enc['labels'] = tokenizer(str(ex['answer']), return_tensors='pt').input_ids
    return enc