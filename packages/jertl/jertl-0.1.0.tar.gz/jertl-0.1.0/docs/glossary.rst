Glossary
========

pattern
    A string describing elements of the jertl mini-language for processing data structures.
    Elements include structures, transforms, collations, and rules.

structures
    Used both for matching and as template for filling.

binding
    A mapping from identifiers to data.

variable
    A reference to data. Variables are represented in mini-language via identifiers.

identifier
    string used to represent a variable in the mini-language.

rule
    sequence of conditions which when satisfied implies a set of actions to be taken.

inference
    describes conditions and results of the application of a rule to data.

vararg
    Mini-language construct indicating that a variable should be bound to a slice of an array.

kwargs
    Construct indicating that a variable could be bound to an object containing key value pairs
    not referenced in the enclosing object structure.

matcher
    Construct defining a condition which is satisfied when a variable matches
    a structure

setter
    Construct defining an action which results in a variable being bound to a filled template

focus
    The data being matched. (see :ref:`The jertl Virtual Machine <Focus Stack>`)
