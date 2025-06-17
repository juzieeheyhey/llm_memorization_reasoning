from .solver import eval_statement
from typing import Any, Dict, List, Tuple

Statement = Any


def extract_refs(stmt: Statement) -> List[int]:
    """Extract person indices referenced in the statement"""
    if not isinstance(stmt, tuple):
        return []
    op = stmt[0]
    if op in ['lying', 'telling-truth']:
        return [stmt[1]]
    refs: List[int] = []
    for s in stmt[1:]:
        refs.extend(extract_refs(s))
    return refs


def reason_puzzle(abstract: Dict) -> List[Tuple[str, Dict]]:
    """Generates abstract reasoning steps"""
    N = abstract['num_people']
    stmts: List[Statement] = abstract['statements']
    steps: List[Tuple[str, Dict]] = []
    exhausted: Dict[int, List[bool]] = {i: [] for i in range(N)}

    def backtrack(assign: Dict[int,bool], queue: List[int]) -> bool:
        if len(assign) == N:
            steps.append(('success', {'assignments': tuple(assign[i] for i in range(N))}))
            return True
        i = queue.pop(0)
        for val in [True, False]:
            if val in exhausted[i]:
                continue
            assign[i] = val
            steps.append(('proposal', {'person': i, 'assignment': val, 'outcome': 'ok'}))
            # Check for contradiction
            conflict_info = None
            for j, stmt in enumerate(stmts):
                if j in assign and assign[j] != eval_statement(stmt, [assign.get(k, False) for k in range(N)]):
                    conflict_info = {'conflict_statement': (j, assign[j])}
                    break
            if conflict_info is not None:
                exhausted[i].append(val)
                info = {'person': i, 'assignment': val, 'outcome': 'conflict'}
                info.update(conflict_info)
                steps.append(('proposal', info))
                queue.insert(0, i)
                continue
            # No conflict: reorder queue based on references
            refs = extract_refs(stmts[i])
            reordered = [p for p in queue if p in refs] + [p for p in queue if p not in refs]
            if backtrack(assign.copy(), reordered.copy()):
                return True
            exhausted[i].append(val)
        # No values left: reconsider
        steps.append(('reconsider', {'person': i, 'exhausted': exhausted[i][:]}))
        assign.pop(i, None)
        queue.insert(0, i)
        return False

    backtrack({}, list(range(N)))
    return steps


