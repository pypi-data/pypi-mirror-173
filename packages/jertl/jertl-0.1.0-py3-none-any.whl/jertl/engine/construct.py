import functools

from ..ast        import representation as jar
from ..exceptions import JertlFillException, JertlPurityException

@functools.singledispatch
def construct(template, _):
    raise JertlFillException(f'build could not handle {template}')

@construct.register(bool)
@construct.register(int)
@construct.register(type(None))
@construct.register(float)
@construct.register(str)
def _(template, _):
    return template

@construct.register(jar.Variable)
def _(template, bindings):
    identifier = template.identifier
    if identifier in bindings:
        return bindings[identifier]
    else:
        raise JertlFillException(f"'{identifier}' not bound")

@construct.register(dict)
def _(template, bindings):
    result = {}
    for key, template in template.items():
        if type(key) == jar.KWArgs:
            result.update(bindings[template.identifier])
        else:
            result[key] = construct(template, bindings)
    #
    return result

@construct.register(list)
def _(template, bindings):
    result = []
    for element in template:
        if isinstance(element, jar.VarArgs):
            result.extend(bindings[element.variable.identifier])
        else:
            result.append(construct(element, bindings))
    return result


@functools.singledispatch
def ensure_purity(value):
    """
    ensure_purity Make sure the data structure we were given is mask free

    Args:
        value: the data structure to inspect

    Raises:
        JertlPurityException: A masked list/dict was found
    """
    raise JertlPurityException(f'purity_check failed {value}')

@ensure_purity.register(bool)
@ensure_purity.register(int)
@ensure_purity.register(type(None))
@ensure_purity.register(float)
@ensure_purity.register(str)
def _(_):
    pass

@ensure_purity.register(list)
def _(value):
    for item in value:
        ensure_purity(item)

@ensure_purity.register(dict)
def _(value):
    for k, v in value.items():
        ensure_purity(k)
        ensure_purity(v)
