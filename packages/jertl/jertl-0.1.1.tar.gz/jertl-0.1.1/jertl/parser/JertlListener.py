# Generated from Jertl.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .JertlParser import JertlParser
else:
    from JertlParser import JertlParser

# This class defines a complete listener for a parse tree produced by JertlParser.
class JertlListener(ParseTreeListener):

    # Enter a parse tree produced by JertlParser#transform.
    def enterTransform(self, ctx:JertlParser.TransformContext):
        pass

    # Exit a parse tree produced by JertlParser#transform.
    def exitTransform(self, ctx:JertlParser.TransformContext):
        pass


    # Enter a parse tree produced by JertlParser#collation.
    def enterCollation(self, ctx:JertlParser.CollationContext):
        pass

    # Exit a parse tree produced by JertlParser#collation.
    def exitCollation(self, ctx:JertlParser.CollationContext):
        pass


    # Enter a parse tree produced by JertlParser#rule_.
    def enterRule_(self, ctx:JertlParser.Rule_Context):
        pass

    # Exit a parse tree produced by JertlParser#rule_.
    def exitRule_(self, ctx:JertlParser.Rule_Context):
        pass


    # Enter a parse tree produced by JertlParser#matcher.
    def enterMatcher(self, ctx:JertlParser.MatcherContext):
        pass

    # Exit a parse tree produced by JertlParser#matcher.
    def exitMatcher(self, ctx:JertlParser.MatcherContext):
        pass


    # Enter a parse tree produced by JertlParser#setter.
    def enterSetter(self, ctx:JertlParser.SetterContext):
        pass

    # Exit a parse tree produced by JertlParser#setter.
    def exitSetter(self, ctx:JertlParser.SetterContext):
        pass


    # Enter a parse tree produced by JertlParser#structure.
    def enterStructure(self, ctx:JertlParser.StructureContext):
        pass

    # Exit a parse tree produced by JertlParser#structure.
    def exitStructure(self, ctx:JertlParser.StructureContext):
        pass


    # Enter a parse tree produced by JertlParser#obj.
    def enterObj(self, ctx:JertlParser.ObjContext):
        pass

    # Exit a parse tree produced by JertlParser#obj.
    def exitObj(self, ctx:JertlParser.ObjContext):
        pass


    # Enter a parse tree produced by JertlParser#key_value.
    def enterKey_value(self, ctx:JertlParser.Key_valueContext):
        pass

    # Exit a parse tree produced by JertlParser#key_value.
    def exitKey_value(self, ctx:JertlParser.Key_valueContext):
        pass


    # Enter a parse tree produced by JertlParser#kwargs.
    def enterKwargs(self, ctx:JertlParser.KwargsContext):
        pass

    # Exit a parse tree produced by JertlParser#kwargs.
    def exitKwargs(self, ctx:JertlParser.KwargsContext):
        pass


    # Enter a parse tree produced by JertlParser#array.
    def enterArray(self, ctx:JertlParser.ArrayContext):
        pass

    # Exit a parse tree produced by JertlParser#array.
    def exitArray(self, ctx:JertlParser.ArrayContext):
        pass


    # Enter a parse tree produced by JertlParser#element.
    def enterElement(self, ctx:JertlParser.ElementContext):
        pass

    # Exit a parse tree produced by JertlParser#element.
    def exitElement(self, ctx:JertlParser.ElementContext):
        pass


    # Enter a parse tree produced by JertlParser#varargs.
    def enterVarargs(self, ctx:JertlParser.VarargsContext):
        pass

    # Exit a parse tree produced by JertlParser#varargs.
    def exitVarargs(self, ctx:JertlParser.VarargsContext):
        pass


    # Enter a parse tree produced by JertlParser#atom.
    def enterAtom(self, ctx:JertlParser.AtomContext):
        pass

    # Exit a parse tree produced by JertlParser#atom.
    def exitAtom(self, ctx:JertlParser.AtomContext):
        pass


    # Enter a parse tree produced by JertlParser#variable.
    def enterVariable(self, ctx:JertlParser.VariableContext):
        pass

    # Exit a parse tree produced by JertlParser#variable.
    def exitVariable(self, ctx:JertlParser.VariableContext):
        pass



del JertlParser