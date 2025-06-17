import copy, random
from .solver import solve_puzzle
from .abstract_module import KKPuzzle
from typing import Dict

MAX_TRIES = 10

def perturb_statement(abstract: Dict) -> Dict:
    """Try up to MAX_TRIES random statement replacements."""
    original_solution = solve_puzzle(abstract)[1]
    for _ in range(MAX_TRIES):
        p = copy.deepcopy(abstract)
        idx = random.randrange(len(p['statements']))
        new_stmt = KKPuzzle(p['num_people'], width=2, depth=2).to_abstract()['statements'][idx]
        p['statements'][idx] = new_stmt

        unique, new_solution = solve_puzzle(p)
        if unique and new_solution != original_solution:
            p['solution'] = new_solution
            return p
    # If all attempts fail, return the original puzzle unmodified
    return abstract

def perturb_leaf(abstract: Dict) -> Dict:
    """Try up to MAX_TRIES random leaf flips; fall back to statement perturbation."""
    original_solution = solve_puzzle(abstract)[1]
    for _ in range(MAX_TRIES):
        p = copy.deepcopy(abstract)
        idx = random.randrange(len(p['statements']))
        # collect all leaf positions in that one statement
        leaves = []
        def collect(stmt, path):
            if stmt[0] in ('lying', 'telling-truth'):
                leaves.append((path, stmt))
            else:
                for i, child in enumerate(stmt[1:], start=1):
                    collect(child, path + [i])
        collect(p['statements'][idx], [])

        if not leaves:
            continue

        path, leaf = random.choice(leaves)
        alt = 'lying' if leaf[0] == 'telling-truth' else 'telling-truth'
        # navigate to the parent of the leaf
        node = p['statements'][idx]
        try:
            for step in path[:-1]:
                node = node[step]
            node[path[-1]] = [alt, leaf[1]]
        except Exception:
            continue

        unique, new_solution = solve_puzzle(p)
        if unique and new_solution != original_solution:
            p['solution'] = new_solution
            return p

    # fallback if leaf perturbation fails
    return perturb_statement(abstract)