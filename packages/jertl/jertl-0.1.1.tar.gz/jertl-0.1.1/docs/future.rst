Future Directions
*****************

New Features
============

Evaluation
----------

In a matching context the result of an evaluation expression is interpreted as a guard
whose truthyness determines whether or not the matching process should continue.

.. code-block::

    company ~ {"employees": [*_, {"age": <<@ > 65>>}, *_]}

The '@' character in the example above refers to the current focus (the value of "age").

In a filling context the result of the evaluation expression is the value inserted into the structure

.. code-block::

    //
    // Do a bit of math
    //

    {"numerator": x, "denominator": y} --> {"quotient": <<x/y>>}


.. code-block:: python

    >> jertl.transform('{"numerator": x, "denominator": y} --> {"quotient": <<x/y>>}', x=1.0, y=2.0).result
    {'quotient': 0.5}


Inline Filters
--------------

.. code-block::

    //
    // Find employees eligible for graduation
    //

    company ~ {"employees": [*_, employee<<{"age": <<@ > 65>>}>>, *_]}

The @ character in the example above refers to the current focus.


Aggregation
-----------

.. code-block::

    //
    // Get list of employee names
    //

    {"employees": employees} --> <<map({"name": name} --> name, employees)>>

This will appear in the same release having Evaluation.
The functions `map`, `filter`, and `reduce`, will be in the set of predefined functions.

Iteration
---------

    The jertl mini-language is 'functional-first' so iteration will not be available.

Disjunction
-----------

    Eventually.

Ecosystem Improvements
======================

    * Semantic analysis to identify potential issues beforehand.
    * Informative Exceptions (location in pattern where exception happened).
    * Editor support for .jertl source files.
    * Structure matching optimization.
    * "Eat our own dogfood" in AST generator and OpCode emitter.
    * Match debugger

Taking it to the Next Level
===========================

Compilation
-----------

.. code-block::

    >>> cat find_highest_paid_male_employee.jertl

    module highest_paid_male
    //
    // Create a Python module with functions is_male, salary, and highest_paid_male_employee
    //
    matcher is_male:
        {"gender": "male"}

    transform salary:
        {"salary": salary} --> salary

    collate highest_paid_male_employee [company]:       \\ Input to this function is a list containing a `company` data structure
        company         ~  {"employees": employees}
        highest_salary :=  <<max(map(age, filter(is_male, employees)))>>
        employees       ~  [*_, employee<<{"salary": highest_salary}>>, *_]

    >>> jertl find_highest_paid_male_employee.jertl -o generated_sources

Rule Sets and Chaining (Forward Inference)
------------------------------------------

Where we consider multiple inference rules simultaneously
and can require there to be sequences of inferences in order for the rule to apply.

.. code-block::

    //
    // Your classic ancestors problem
    //
    ruleset ancestors
        rule find_ancestors [person]:
            person ~ {"parents": [mother, father]}
          -->
            O=O=O ancestors [person, mother]    // `O=O=O`: chain to ancestors ruleset
            O=O=O ancestors [person, father]

        rule note_ancestry_and_look_deeper [person, ancestor]:
            person ~ {"name": person_name},
            ancestor ~ {"name": ancestor_name, "parents": [ancestors_mother, ancestors_father]}
          -->
            ancestry := {"person": person_name, "ancestor": ancestor_name}
            O=O=O ancestors [person, ancestors_mother]
            O=O=O ancestors [person, ancestors_father]

        rule no_more_birth_records [person, parent]:
            person ~ {"name": person_name},
            ancestor ~ {"name": ancestor_name, "parents": null}
          -->
            ancestry := {"person": person_name, "ancestor": ancestor_name}

Working Memory
--------------

Where working memory is a key/value store.

.. code-block::

    rule supervises [supervisor, employee]
        supervisor ~ {"name": supervisor_name, "underlings": [\*_, employee, \*_]}
        employee@  ~ {"name": underling_name}      // <-- `employee` is bound to string which points to data in working memory.
                                                   //     The data is retrieved and the matching process continued.
        -->
        supervises := [supervisor_name, underling_name]

Moonshots
=========

Data Stores
-----------

Where data is external to Python.

.. code-block::

    rule is_supervisor [supervisor, employee]
        supervisor@sql_employee_table ~ {"name": supervisor_name, "underlings": [\*_, employee, \*_]}
        employee@sql_employee_table   ~ {"name": underling_name}      // employee is key to data stored in a SQL table
        -->
        supervises := [supervisor_name, underling_name]

Mutation
--------

    Where we mutate a data structure using overlays.
    What is an overlay you ask?
    Good question! Overlays and how they work need to be formally defined.

.. code-block::

    rule record_change_of_supervisor [employee_id, previous_supervisor, new_supervisor]
      -->
        previous_supervisor :- {"underlings": [*_, employee_id, *_]}  // <-- remove portion of data structure matching overlay
        new_supervisor      :+ {"underlings": [*_, employee_id]}      // <-- add data described by overlay
