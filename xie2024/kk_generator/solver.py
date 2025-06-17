import itertools
from typing import Any, Dict, List, Tuple

Statement = Any

def eval_statement(stmt: Statement, assignment: List[bool]) -> bool:
    op = stmt[0]
    if op == 'telling-truth': return assignment[stmt[1]]
    if op == 'lying': return not assignment[stmt[1]]
    if op == 'and': return all(eval_statement(s, assignment) for s in stmt[1:])
    if op == 'or': return any(eval_statement(s, assignment) for s in stmt[1:])
    if op == '->': return (not eval_statement(stmt[1], assignment)) or eval_statement(stmt[2], assignment)
    if op == '<=>': return eval_statement(stmt[1], assignment) == eval_statement(stmt[2], assignment)
    return False


def solve_puzzle(abstract: Dict) -> Tuple[bool, List[bool]]:
    N = abstract['num_people']
    stmts = abstract['statements']
    solutions: List[List[bool]] = []
    for bits in itertools.product([False, True], repeat=N):
        if all(bits[i] == eval_statement(stmts[i], list(bits)) for i in range(N)):
            solutions.append(list(bits))
    return (len(solutions) == 1, solutions[0] if len(solutions) == 1 else [])

