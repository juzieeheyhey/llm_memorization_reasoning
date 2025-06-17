import json
from kk_generator.perturbation import perturb_statement
from kk_generator.solver import solve_puzzle
from evaluation.evaluate_accuracy import main as eval_acc

def main():
    data = json.load(open('data/processed/test.json'))
    orig_count = 0
    consistent = 0
    for ex in data:
        # original abstract puzzle
        abstract = ex['abstract']
        unique, sol = solve_puzzle(abstract)
        if not unique:
            continue
        orig_count += 1
        # apply statement-level perturbation
        perturbed = perturb_statement(abstract)
        uniq2, sol2 = solve_puzzle(perturbed)
        # count as consistent if model would still solve it
        if uniq2 and sol2 != sol:
            # changed solution => inconsistent
            pass
        else:
            consistent += 1
    ratio = consistent / orig_count if orig_count > 0 else 0.0
    print(f"Consistency ratio: {ratio:.4f}")
    return ratio

if __name__=='__main__':
    main()