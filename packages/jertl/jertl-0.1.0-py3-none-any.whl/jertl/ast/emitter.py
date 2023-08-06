import functools

from ..engine.opcodes import OpCode
from .                import representation as jar
from ..exceptions     import JertlCodeEmitterException

@functools.singledispatch
def emit(structure, _):
    raise JertlCodeEmitterException(f'emit cannot handle {structure}')

@emit.register(int)
@emit.register(float)
@emit.register(str)
@emit.register(bool)
@emit.register(type(None))
def _(structure, _):
    yield OpCode.MATCH_VALUE, structure

@emit.register(jar.Variable)
def _(variable, bindings):
    identifier = variable.identifier
    if identifier in bindings:
        yield OpCode.MATCH_VARIABLE, identifier
    else:
        yield OpCode.BIND_VARIABLE, identifier
        bindings |= {identifier}

@emit.register(jar.VarArgs)
def _(varargs, bindings):
    identifier = varargs.variable.identifier
    if identifier in bindings:
        yield OpCode.MATCH_VARARGS, identifier
    else:
        yield OpCode.BIND_VARARGS, identifier
        bindings |= {identifier}

@emit.register(dict)
def _(dict_, bindings):
    yield OpCode.MASK_IF_DICT,

    kwargs = None
    for key, structure in dict_.items():
        if type(key) == jar.KWArgs:
            # The KWArgs variable must be processed after the other keys
            kwargs = structure
        else:
            yield OpCode.FOCUS_ON_KEY, key
            yield from emit(structure, bindings)
            yield OpCode.POP_FOCUS,

    if kwargs is not None:
        yield from emit(kwargs, bindings)

@emit.register(list)
def _(array, bindings):
    yield OpCode.MASK_IF_LIST,

    for element in array:
        if isinstance(element, jar.VarArgs):
            yield from emit(element, bindings)
        else:
            yield OpCode.FOCUS_ON_HEAD,
            yield from emit(element, bindings)
            yield OpCode.POP_FOCUS,

    yield OpCode.MATCH_VALUE, []

def optimize_splats(instructions):
    splat = None

    #
    # This is ugly and will remain so intentionlly as incentive to use jertl for peephole optimization
    # (AKA the "Eat my own dogfood initiative")
    #
    for instruction in instructions:
        if splat is not None:
            # Previous opcode was a splat.
            # If we are matching focus to the empty list
            # we can optimize away the push to context stack
            if instruction == (OpCode.MATCH_VALUE, []):
                yield OpCode.BIND_VARIABLE, splat[1]
                splat = None
            else:
                yield splat
                splat = None
                if instruction[0] == OpCode.BIND_VARARGS:
                    #
                    # Need to handle the case [[BIND_VARARGS, var1], [BIND_VARARGS, var2], [MATCH_VALUE, []]]
                    #
                    splat = instruction
                else:
                    yield instruction

        elif instruction[0] == OpCode.BIND_VARARGS:
            splat = instruction
        else:
            yield instruction

def emit_match(structure):
    bindings = set()
    yield from optimize_splats(emit(structure, bindings))
    yield OpCode.YIELD_BINDINGS,

def emit_collation(collation, initial_bindings):
    for matcher in collation:
        yield OpCode.FOCUS_ON_BINDING, matcher.variable.identifier
        yield from optimize_splats(emit(matcher.structure, initial_bindings))

    for _ in collation:
        yield OpCode.POP_FOCUS,

    yield OpCode.YIELD_BINDINGS,
