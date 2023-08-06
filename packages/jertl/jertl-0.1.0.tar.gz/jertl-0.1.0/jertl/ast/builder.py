import antlr4
from antlr4.error.Errors import ParseCancellationException

from jertl.exceptions import JertlSyntaxError

from .  import representation as jar
from .  import helpers        as helpers
from .. import parser         as jp

class JertlBuilder(helpers.ASTBuilder, jp.Listener):

    def exitTransform(self, ctx):
        ctx.AST = jar.Transform(input=ctx.structure(0).AST,
                                output=ctx.structure(1).AST)

    def exitCollation(self, ctx):
        ctx.AST = self.ASTsOf(ctx.matcher())

    def exitRule_(self, ctx):
        ctx.AST = jar.Rule(matchers=self.ASTsOf(ctx.matcher()),
                           setters=self.ASTsOf(ctx.setter()))

    def exitMatcher(self, ctx):
        ctx.AST = jar.Matcher(ctx.variable().AST, ctx.structure().AST)

    def exitSetter(self, ctx):
        ctx.AST = jar.Setter(ctx.variable().AST, ctx.structure().AST)

    def exitStructure(self, ctx):
        ctx.AST = self.whichOf(ctx.obj(),
                               ctx.array(),
                               ctx.atom(),
                               ctx.variable()).AST

    def exitObj(self, ctx):
        ast = dict(self.ASTsOf(ctx.key_values))
        if ctx.kwargs() is not None:
            ast[jar.KWArgs()] = ctx.kwargs().AST
        ctx.AST = ast

    def exitKey_value(self, ctx):
        ctx.AST = (self.dequote(ctx.STRING().getText()), ctx.structure().AST)

    def exitKwargs(self, ctx):
        ctx.AST = ctx.variable().AST

    def exitArray(self, ctx):
        ctx.AST = self.ASTsOf(ctx.elements)

    def exitElement(self, ctx):
        ctx.AST = self.whichOf(ctx.structure(), ctx.varargs()).AST

    def exitVarargs(self, ctx):
        ctx.AST = jar.VarArgs(ctx.variable().AST)

    def exitAtom(self, ctx):
        if ctx.NULL() is not None:
            ctx.AST = None
        elif ctx.TRUE() is not None:
            ctx.AST = True
        elif ctx.FALSE() is not None:
            ctx.AST = False
        elif ctx.INTEGER() is not None:
            ctx.AST = int(ctx.INTEGER().getText())
        elif ctx.FLOAT() is not None:
            ctx.AST = float(ctx.FLOAT().getText())
        elif ctx.STRING() is not None:
            ctx.AST = self.dequote(ctx.STRING().getText())

    def exitVariable(self, ctx):
        ctx.AST = jar.Variable(ctx.IDENTIFIER().getText())

    def dequote(self, s):
        if s.endswith('"'):
            s = s[:-1]
        if s.startswith('"'):
            s = s[1:]
        return s

def string_parser(string):
    input_stream = antlr4.InputStream(string)
    lexer = jp.Lexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(helpers.ThrowingErrorListener())

    token_stream = antlr4.CommonTokenStream(lexer)

    parser = jp.Parser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(helpers.ThrowingErrorListener())
    #
    return parser

def parse_string(string, rulename):
    parser = string_parser(string)
    rule   = getattr(parser, rulename)
    tree   = rule()
    return tree

def ast_from_tree(tree, trace=False):
    builder = JertlBuilder(trace=trace)
    walker  = antlr4.ParseTreeWalker()
    walker.walk(builder, tree)
    return tree.AST

def ast_for_string(string, rulename, trace=False):
    return ast_from_tree(parse_string(string, rulename), trace=trace)
