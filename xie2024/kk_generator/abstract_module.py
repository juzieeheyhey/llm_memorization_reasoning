import random
from typing import Any, List

LOGICAL_OPS = ['and', 'or', '->', '<=>']
LEAF_OPS = ['lying', 'telling-truth']

from typing import Any  

class KKPerson:
    def __init__(self, index: int):
        self.index = index
        self.statement: Any = None

class KKPuzzle:
    def __init__(self, num_people: int, width: int = 2, depth: int = 2):
        self.num_people = num_people
        self.width = width
        self.depth = depth
        self.people: List[KKPerson] = [KKPerson(i) for i in range(num_people)]
        self.generate_statements()

    def generate_statements(self):
        for person in self.people:
            person.statement = self.sample_statement(0)

    def sample_statement(self, current_depth: int) -> Any:
        if current_depth >= self.depth:
            op = random.choice(LEAF_OPS)
            target = random.randrange(self.num_people)
            return (op, target)
        
        if random.random() < 0.5:
            op = random.choice(LEAF_OPS)
            target = random.randrange(self.num_people)
            return (op, target)
        
        op = random.choice(LOGICAL_OPS)
        num_children = random.randint(2, self.width)
        children = []
        for _ in range(num_children):
            stmt = self.sample_statement(current_depth + 1)
            children.append(stmt)
        return (op, *children)

    def to_abstract(self) -> dict:
        return {
            'num_people': self.num_people,
            'statements': [p.statement for p in self.people if p.statement is not None]
        }


