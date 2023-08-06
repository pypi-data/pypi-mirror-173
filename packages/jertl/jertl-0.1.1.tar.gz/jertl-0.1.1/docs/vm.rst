The jertl Virtual Machine
=========================

Architecture
------------
.. figure:: vm.png

Context Stack
^^^^^^^^^^^^^

When binding the variable of a splat expression the vm progressively includes larger slices of the list being examined.
This is implemented using backtracking. When first matching an unbound binding splat expression to a list, the vm takes a snapshot
of the vm's state and pushes it onto the context stack. The variable of the splat expression is then bound to an empty list.

On backtrack the vm uses the snapshot at the top of the context stack to restore state,
widens the splat variable's binding to include the next element of the list, then continues execution.
If there are no more elements in the list the snapshot is popped off the context stack and the vm again backtracks.
The vm halts if the context stack is empty.

.. _Focus Stack:

Focus Stack
^^^^^^^^^^^

The focus stack holds the structured data being processed.
For the match and transform operations the data argument is the first item pushed onto the stack.
This stack grows as the vm examines deeper items of a data structure or switches to different data via a targetted match.

Masking
^^^^^^^

Masks are thin wrappers used by the VM to mark off items in lists and dicts which have been matched.
The intent is to avoid destructive modification of input data, excessive copying, and to make the code a bit more readable.

Opcodes
-------
+----------------------+-------------------------------+--------------------------------------------------------------------------+
+ OpCode               | Argument                      | Action                                                                   |
+======================+===============================+==========================================================================+
|    MATCH_VALUE       | A value to compre to focus    | Compares value to focus, backtrack if no match.                          |
+----------------------+-------------------------------+--------------------------------------------------------------------------+
|    BIND_VARIABLE     | Identifier                    | Bind identifier to focus.                                                |
+----------------------+-------------------------------+--------------------------------------------------------------------------+
|    MATCH_VARIABLE    | Identifier                    | Compares binding of identifier to focus, backtrack if no match.          |
+----------------------+-------------------------------+--------------------------------------------------------------------------+
|    BIND_VARARGS      | Identifier                    | Push snapshot of virtual machine and onto context stack.                 |
|                      |                               | Sets initial binding of identifier to an empty list.                     |
+----------------------+-------------------------------+--------------------------------------------------------------------------+
|    MATCH_VARARGS     | Identifier                    | Check if focus starts with binding of identifier, backtrack if no match. |
+----------------------+-------------------------------+--------------------------------------------------------------------------+
|    MASK_IF_LIST      | <none>                        | If focus is a list mask it, otherwise backtrack.                         |
+----------------------+-------------------------------+--------------------------------------------------------------------------+
|    MASK_IF_DICT      | <none>                        | If focus is a dict mask it, otherwise backtrack.                         |
+----------------------+-------------------------------+--------------------------------------------------------------------------+
|    FOCUS_ON_HEAD     | <none>                        | Push first item of list onto focus stack, backtrack if list is empty.    |
+----------------------+-------------------------------+--------------------------------------------------------------------------+
|    FOCUS_ON_KEY      | Key                           | Push value of dict key onto focus stack, backtrack if key not present.   |
+----------------------+-------------------------------+--------------------------------------------------------------------------+
|    FOCUS_ON_BINDING  | Identifier                    | Push variable binding onto focus stack.                                  |
+----------------------+-------------------------------+--------------------------------------------------------------------------+
|    POP_FOCUS         | <none>                        | Pop focus stack.                                                         |
+----------------------+-------------------------------+--------------------------------------------------------------------------+
|    YIELD_BINDINGS    | <none>                        | Yield copy of current bindings then backtrack.                           |
+----------------------+-------------------------------+--------------------------------------------------------------------------+
