
class JertlSyntaxError(RuntimeError):
    """
    JertlSyntaxError Error in mini-language source
    """


class JertlInterpreterException (Exception):
    pass

class JertlCodeEmitterException (Exception):
    pass

class JertlFillException (Exception):
    """
    JertlFillException Reference to unbound variable during a fill operation
    """

class JertlPurityException (Exception):
    pass
