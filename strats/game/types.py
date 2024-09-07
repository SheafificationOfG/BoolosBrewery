"""
Game question API
"""
from collections.abc import Mapping as _Mapping

class Expr:

    def __init__(self, value):
        match value:
            case bool():
                self._value = str(value).lower()
            case int():
                assert(value in [0, 1])
                self._value = str(value)
            case _:
                self._value = str(value)
    
    def __str__(self):
        return self._value
    
    def invert(self):
        return Expr(f"not {self}")

    def and_(self, other):
        return Expr(f"({self} and {other})")
    
    def or_(self, other):
        return Expr(f"({self} or {other})")
    
    def implies(self, other):
        return Expr(f"({self} implies {other})")
    
    def iff(self, other):
        return Expr(f"({self} iff {other})")
    
    def xor(self, other):
        return Expr(f"({self} xor {other})")

    def __invert__(self):
        return self.invert()
    
    def __and__(self, other):
        return self.and_(other)
    
    def __or__(self, other):
        return self.or_(other)
    
    def __bool__(self):
        raise TypeError(f"Implicit cast of expression {self} into a Boolean!")

class Person:

    def __init__(self, name, index: int):
        self._name = name
        self._index = index

    def __int__(self):
        return self._index
    
    def __str__(self):
        return self._name
    
    def __hash__(self):
        return hash(str(self))
    
    def studies(self, field):
        return Expr(f"{self} studies {field}")
    
    def ask(self, expr: Expr):
        return Question(self, expr)
    
    def __call__(self, expr: Expr):
        return self.ask(expr)

class Field:

    def __init__(self, name):
        self._name = name
    
    def __str__(self):
        return self._name

    def __hash__(self):
        return hash(str(self))

class Response:

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return self._name
    
    def __hash__(self):
        return hash(str(self))
        
    def equals(self, other):
        return Expr(f"({self} is {other})")
    
    def not_equals(self, other):
        return Expr(f"({self} not {other})")

class Question(Response):

    def __init__(self, person: Person, expr):
        self.person = person
        self.expr = expr

    def __str__(self):
        return f"\"{self.person}: {self.expr}?\""
    
class Guesses(_Mapping):

    def __init__(self):
        self.Alice = None
        self.Bob = None
        self.Charlie = None
        self.Dan = None

    def __getitem__(self, person: Person):
        if isinstance(person, Person):
            person = str(person)
        return getattr(self, str(person))
    
    def __setitem__(self, person: Person, value: Field|None):
        if isinstance(person, Person):
            person = str(person)
        setattr(self, str(person), value)
    
    def __len__(self):
        return [self.Alice, self.Bob, self.Charlie, self.Dan, None].index(None)
    
    def __iter__(self):
        for name in ["Alice", "Bob", "Charlie", "Dan"]:
            if getattr(self, name) is not None:
                yield name
            else:
                break
            