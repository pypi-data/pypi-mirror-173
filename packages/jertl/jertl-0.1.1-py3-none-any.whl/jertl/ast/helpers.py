import antlr4

from ..exceptions import JertlSyntaxError

from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import ParseCancellationException

class ThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        ex = JertlSyntaxError(f'line {line}: {column} {msg}')
        ex.line = line
        ex.column = column
        raise ex

def remove_suffix(string, suffix):
    if string.endswith(suffix):
        return string[:-len(suffix)]
    else:
        return string

class TracingListener(antlr4.ParseTreeListener):
    def __init__(self, *varargs, trace=False, **kwargs):
        self._level = 0
        self._trace = trace
        super().__init__(*varargs, **kwargs)

    def context2name(self, ctx):
        return remove_suffix(type(ctx).__name__.split('.')[-1], 'Context')

    def enterEveryRule(self, ctx):
        if self._trace:
            print(' '*self._level, '-->', self.context2name(ctx))
            self._level += 1
        #
        super().enterEveryRule(ctx)

    def exitEveryRule(self, ctx):
        name = self.context2name(ctx)
        if self._trace:
            self._level -= 1
            print(' '*self._level, '<--', name)
        #
        super().exitEveryRule(ctx)

# For use by Listeners generating ASTs
class ASTBuilder(TracingListener):
    def __init__(self, *varargs, ignore_missing=False, **kwargs):
        self.ignore_missing = ignore_missing
        super().__init__(*varargs, **kwargs)

    def exitEveryRule(self, ctx):
        self.checkHasAst(ctx)
        super().exitEveryRule(ctx)

    def checkHasAst(self, ctx):
        if not hasattr(ctx, 'AST') and not self.ignore_missing:
            raise Exception(self.context2name(ctx), 'has no AST')
        else:
            return True

    def _AST(self, context):
        if self.ignore_missing:
            return getattr(context, 'AST', None)
        else:
            return context.AST

    def ASTsOf(self, contexts):
        return [self._AST(c) for c in contexts]

    def whichOf(self, *contexts):
        for ctx in contexts:
            if ctx is not None:
                return ctx

    def optional(self, ctx):
        if ctx is not None:
            return self._AST(ctx)
