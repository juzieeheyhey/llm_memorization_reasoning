from evaluation.evaluate_accuracy import main as eval_acc
from evaluation.compute_consistency import main as eval_cons

def main():
    acc = eval_acc()
    cr  = eval_cons()
    print(f"LiMem: {acc*(1-cr):.4f}")

if __name__=='__main__': 
    main()