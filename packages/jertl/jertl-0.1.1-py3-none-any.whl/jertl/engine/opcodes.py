import enum

class OpCode(enum.Enum):
    MATCH_VALUE      = enum.auto()
    BIND_VARIABLE    = enum.auto()
    MATCH_VARIABLE   = enum.auto()

    BIND_VARARGS     = enum.auto()
    MATCH_VARARGS    = enum.auto()

    MASK_IF_LIST     = enum.auto()
    MASK_IF_DICT     = enum.auto()
    
    FOCUS_ON_HEAD    = enum.auto()
    FOCUS_ON_KEY     = enum.auto()
    FOCUS_ON_BINDING = enum.auto()
    POP_FOCUS        = enum.auto()

    YIELD_BINDINGS   = enum.auto()

    def __repr__(self):
        return self.name