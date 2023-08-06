from dataclasses import dataclass, field
from typing      import Dict, List, Union

@dataclass
class Variable:
    identifier: str
    anonymous:  bool = field(init=False, default=False)
    #
    anon_counter = 0

    def __post_init__(self):
        if self.identifier == '_':
            Variable.anon_counter += 1
            self.anonymous = True
            self.identifier = f'$_{Variable.anon_counter}'

    def __repr__(self):
        return self.identifier if not self.anonymous else '_'

@dataclass
class VarArgs:
    variable: Variable

## Used by emitter to identify KWArgs in a dictionary
class KWArgs:
    def __repr__(self):
        return '<KWArgs>'

    ## Equality and hash used by pytest cases
    def __eq__(self, other):
        return type(other) == KWArgs

    def __hash__(self):
        return hash(repr(self))

Structure = Union[List, Dict, str, int, float, bool, type(None)]

@dataclass
class Transform:
    input:  Structure
    output: Structure

@dataclass
class Matcher:
    variable:  Variable
    structure: Structure

@dataclass
class Setter:
    variable:  Variable
    structure: Structure

@dataclass
class Rule:
    matchers: List[Matcher]
    setters:  List[Setter]
