import json
import yaml
from transformers.pipelines import pipeline

cfg = yaml.safe_load(open('config/config.yaml'))

def main():
    data = json.load(open('data/processed/test.json'))
    gen = pipeline('text-generation', model='models/llama_finetune/direct')
    correct = 0
    for ex in data:
        q = ''.join(ex['question'])
        results = gen(q, max_length=cfg['max_len'])
        if not isinstance(results, list) or len(results) == 0:
            continue
        out_str = results[0].get('generated_text', '')
        out_str = str(out_str)
        if out_str.strip().endswith(str(ex['answer'])):
            correct += 1
    total = len(data)
    acc = correct / total if total > 0 else 0.0
    print(f"Accuracy: {acc:.4f}")
    return acc

if __name__=='__main__':
    main()