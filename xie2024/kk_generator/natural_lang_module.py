import random
from typing import Any, Dict, List
from .reasoner import reason_puzzle

COMMON_NAMES = ['Emma','Liam','Olivia','Noah','Ava','Ethan','Sophia','Mason','Isabella',
                'William','Mia','James','Charlotte','Benjamin','Amelia','Lucas','Harper',
                'Henry','Evelyn','Alexander','Abigail','Michael','Emily','Daniel','Elizabeth',
                'Jacob','Sofia','Logan','Avery','Jackson','Ella']

TEMPLATES = ["{i} says: '{sub}.'", "In {i}'s words: '{sub}.'"]


def template_from_stmt(stmt: Any, names: List[str]) -> str:
    op = stmt[0]
    if op in ['lying','telling-truth']:
        target = names[stmt[1]]
        verb = 'is truthful' if op=='telling-truth' else 'always lies'
        return f"{target} {verb}"
    if op=='and': return ' and '.join(template_from_stmt(s,names) for s in stmt[1:])
    if op=='or': return ' or '.join(template_from_stmt(s,names) for s in stmt[1:])
    if op=='->': return f"if {template_from_stmt(stmt[1],names)}, then {template_from_stmt(stmt[2],names)}"
    if op=='<=>': return f"{template_from_stmt(stmt[1],names)} if and only if {template_from_stmt(stmt[2],names)}"
    return ''


def render_puzzle(abstract: Dict, solution: List[bool]) -> Dict[str, Any]:
    N = abstract['num_people']
    names = random.sample(COMMON_NAMES, N)
    question = [f"This is a puzzle with {N} people: {', '.join(names)}."]
    for idx, stmt in enumerate(abstract['statements']):
        sub = template_from_stmt(stmt, names)
        question.append(random.choice(TEMPLATES).format(i=names[idx], sub=sub))
    answer = {names[i]: 'Knight' if solution[i] else 'Knave' for i in range(N)}
    # Convert reasoning steps to strings for readability
    raw_steps = reason_puzzle(abstract)
    reasoning = [f"{step_type}: {info}" for step_type, info in raw_steps]
    return {'question': question, 'answer': answer, 'reasoning': reasoning}

