# Generated from Jertl.g4 by ANTLR 4.11.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,20,118,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        1,0,1,0,1,0,1,0,1,1,5,1,34,8,1,10,1,12,1,37,9,1,1,2,5,2,40,8,2,10,
        2,12,2,43,9,2,1,2,1,2,5,2,47,8,2,10,2,12,2,50,9,2,1,3,1,3,1,3,1,
        3,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,3,5,64,8,5,1,6,1,6,1,6,1,6,5,6,
        70,8,6,10,6,12,6,73,9,6,1,6,1,6,3,6,77,8,6,1,6,1,6,1,6,1,6,3,6,83,
        8,6,1,7,1,7,1,7,1,7,1,8,1,8,1,8,1,9,1,9,1,9,1,9,5,9,96,8,9,10,9,
        12,9,99,9,9,1,9,1,9,1,9,1,9,3,9,105,8,9,1,10,1,10,3,10,109,8,10,
        1,11,1,11,1,11,1,12,1,12,1,13,1,13,1,13,0,0,14,0,2,4,6,8,10,12,14,
        16,18,20,22,24,26,0,1,2,0,10,13,17,18,115,0,28,1,0,0,0,2,35,1,0,
        0,0,4,41,1,0,0,0,6,51,1,0,0,0,8,55,1,0,0,0,10,63,1,0,0,0,12,82,1,
        0,0,0,14,84,1,0,0,0,16,88,1,0,0,0,18,104,1,0,0,0,20,108,1,0,0,0,
        22,110,1,0,0,0,24,113,1,0,0,0,26,115,1,0,0,0,28,29,3,10,5,0,29,30,
        5,9,0,0,30,31,3,10,5,0,31,1,1,0,0,0,32,34,3,6,3,0,33,32,1,0,0,0,
        34,37,1,0,0,0,35,33,1,0,0,0,35,36,1,0,0,0,36,3,1,0,0,0,37,35,1,0,
        0,0,38,40,3,6,3,0,39,38,1,0,0,0,40,43,1,0,0,0,41,39,1,0,0,0,41,42,
        1,0,0,0,42,44,1,0,0,0,43,41,1,0,0,0,44,48,5,9,0,0,45,47,3,8,4,0,
        46,45,1,0,0,0,47,50,1,0,0,0,48,46,1,0,0,0,48,49,1,0,0,0,49,5,1,0,
        0,0,50,48,1,0,0,0,51,52,3,26,13,0,52,53,5,14,0,0,53,54,3,10,5,0,
        54,7,1,0,0,0,55,56,3,26,13,0,56,57,5,15,0,0,57,58,3,10,5,0,58,9,
        1,0,0,0,59,64,3,12,6,0,60,64,3,18,9,0,61,64,3,24,12,0,62,64,3,26,
        13,0,63,59,1,0,0,0,63,60,1,0,0,0,63,61,1,0,0,0,63,62,1,0,0,0,64,
        11,1,0,0,0,65,66,5,1,0,0,66,71,3,14,7,0,67,68,5,2,0,0,68,70,3,14,
        7,0,69,67,1,0,0,0,70,73,1,0,0,0,71,69,1,0,0,0,71,72,1,0,0,0,72,76,
        1,0,0,0,73,71,1,0,0,0,74,75,5,2,0,0,75,77,3,16,8,0,76,74,1,0,0,0,
        76,77,1,0,0,0,77,78,1,0,0,0,78,79,5,3,0,0,79,83,1,0,0,0,80,81,5,
        1,0,0,81,83,5,3,0,0,82,65,1,0,0,0,82,80,1,0,0,0,83,13,1,0,0,0,84,
        85,5,13,0,0,85,86,5,4,0,0,86,87,3,10,5,0,87,15,1,0,0,0,88,89,5,5,
        0,0,89,90,3,26,13,0,90,17,1,0,0,0,91,92,5,6,0,0,92,97,3,20,10,0,
        93,94,5,2,0,0,94,96,3,20,10,0,95,93,1,0,0,0,96,99,1,0,0,0,97,95,
        1,0,0,0,97,98,1,0,0,0,98,100,1,0,0,0,99,97,1,0,0,0,100,101,5,7,0,
        0,101,105,1,0,0,0,102,103,5,6,0,0,103,105,5,7,0,0,104,91,1,0,0,0,
        104,102,1,0,0,0,105,19,1,0,0,0,106,109,3,10,5,0,107,109,3,22,11,
        0,108,106,1,0,0,0,108,107,1,0,0,0,109,21,1,0,0,0,110,111,5,8,0,0,
        111,112,3,26,13,0,112,23,1,0,0,0,113,114,7,0,0,0,114,25,1,0,0,0,
        115,116,5,16,0,0,116,27,1,0,0,0,10,35,41,48,63,71,76,82,97,104,108
    ]

class JertlParser ( Parser ):

    grammarFileName = "Jertl.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "','", "'}'", "':'", "'**'", "'['", 
                     "']'", "'*'", "'-->'", "'null'", "'true'", "'false'", 
                     "<INVALID>", "'~'", "':='" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "IMPLIES", "NULL", "TRUE", "FALSE", "STRING", 
                      "MATCHES", "ASSIGNED", "IDENTIFIER", "INTEGER", "FLOAT", 
                      "WS", "LINE_COMMENT" ]

    RULE_transform = 0
    RULE_collation = 1
    RULE_rule_ = 2
    RULE_matcher = 3
    RULE_setter = 4
    RULE_structure = 5
    RULE_obj = 6
    RULE_key_value = 7
    RULE_kwargs = 8
    RULE_array = 9
    RULE_element = 10
    RULE_varargs = 11
    RULE_atom = 12
    RULE_variable = 13

    ruleNames =  [ "transform", "collation", "rule_", "matcher", "setter", 
                   "structure", "obj", "key_value", "kwargs", "array", "element", 
                   "varargs", "atom", "variable" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    IMPLIES=9
    NULL=10
    TRUE=11
    FALSE=12
    STRING=13
    MATCHES=14
    ASSIGNED=15
    IDENTIFIER=16
    INTEGER=17
    FLOAT=18
    WS=19
    LINE_COMMENT=20

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.11.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class TransformContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def structure(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JertlParser.StructureContext)
            else:
                return self.getTypedRuleContext(JertlParser.StructureContext,i)


        def IMPLIES(self):
            return self.getToken(JertlParser.IMPLIES, 0)

        def getRuleIndex(self):
            return JertlParser.RULE_transform

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTransform" ):
                listener.enterTransform(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTransform" ):
                listener.exitTransform(self)




    def transform(self):

        localctx = JertlParser.TransformContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_transform)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 28
            self.structure()
            self.state = 29
            self.match(JertlParser.IMPLIES)
            self.state = 30
            self.structure()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CollationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def matcher(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JertlParser.MatcherContext)
            else:
                return self.getTypedRuleContext(JertlParser.MatcherContext,i)


        def getRuleIndex(self):
            return JertlParser.RULE_collation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCollation" ):
                listener.enterCollation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCollation" ):
                listener.exitCollation(self)




    def collation(self):

        localctx = JertlParser.CollationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_collation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 32
                self.matcher()
                self.state = 37
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Rule_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IMPLIES(self):
            return self.getToken(JertlParser.IMPLIES, 0)

        def matcher(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JertlParser.MatcherContext)
            else:
                return self.getTypedRuleContext(JertlParser.MatcherContext,i)


        def setter(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JertlParser.SetterContext)
            else:
                return self.getTypedRuleContext(JertlParser.SetterContext,i)


        def getRuleIndex(self):
            return JertlParser.RULE_rule_

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRule_" ):
                listener.enterRule_(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRule_" ):
                listener.exitRule_(self)




    def rule_(self):

        localctx = JertlParser.Rule_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_rule_)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 38
                self.matcher()
                self.state = 43
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 44
            self.match(JertlParser.IMPLIES)
            self.state = 48
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 45
                self.setter()
                self.state = 50
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MatcherContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variable(self):
            return self.getTypedRuleContext(JertlParser.VariableContext,0)


        def MATCHES(self):
            return self.getToken(JertlParser.MATCHES, 0)

        def structure(self):
            return self.getTypedRuleContext(JertlParser.StructureContext,0)


        def getRuleIndex(self):
            return JertlParser.RULE_matcher

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMatcher" ):
                listener.enterMatcher(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMatcher" ):
                listener.exitMatcher(self)




    def matcher(self):

        localctx = JertlParser.MatcherContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_matcher)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self.variable()
            self.state = 52
            self.match(JertlParser.MATCHES)
            self.state = 53
            self.structure()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SetterContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variable(self):
            return self.getTypedRuleContext(JertlParser.VariableContext,0)


        def ASSIGNED(self):
            return self.getToken(JertlParser.ASSIGNED, 0)

        def structure(self):
            return self.getTypedRuleContext(JertlParser.StructureContext,0)


        def getRuleIndex(self):
            return JertlParser.RULE_setter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSetter" ):
                listener.enterSetter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSetter" ):
                listener.exitSetter(self)




    def setter(self):

        localctx = JertlParser.SetterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_setter)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self.variable()
            self.state = 56
            self.match(JertlParser.ASSIGNED)
            self.state = 57
            self.structure()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StructureContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def obj(self):
            return self.getTypedRuleContext(JertlParser.ObjContext,0)


        def array(self):
            return self.getTypedRuleContext(JertlParser.ArrayContext,0)


        def atom(self):
            return self.getTypedRuleContext(JertlParser.AtomContext,0)


        def variable(self):
            return self.getTypedRuleContext(JertlParser.VariableContext,0)


        def getRuleIndex(self):
            return JertlParser.RULE_structure

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStructure" ):
                listener.enterStructure(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStructure" ):
                listener.exitStructure(self)




    def structure(self):

        localctx = JertlParser.StructureContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_structure)
        try:
            self.state = 63
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 59
                self.obj()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 60
                self.array()
                pass
            elif token in [10, 11, 12, 13, 17, 18]:
                self.enterOuterAlt(localctx, 3)
                self.state = 61
                self.atom()
                pass
            elif token in [16]:
                self.enterOuterAlt(localctx, 4)
                self.state = 62
                self.variable()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObjContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._key_value = None # Key_valueContext
            self.key_values = list() # of Key_valueContexts

        def key_value(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JertlParser.Key_valueContext)
            else:
                return self.getTypedRuleContext(JertlParser.Key_valueContext,i)


        def kwargs(self):
            return self.getTypedRuleContext(JertlParser.KwargsContext,0)


        def getRuleIndex(self):
            return JertlParser.RULE_obj

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObj" ):
                listener.enterObj(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObj" ):
                listener.exitObj(self)




    def obj(self):

        localctx = JertlParser.ObjContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_obj)
        self._la = 0 # Token type
        try:
            self.state = 82
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 65
                self.match(JertlParser.T__0)
                self.state = 66
                localctx._key_value = self.key_value()
                localctx.key_values.append(localctx._key_value)
                self.state = 71
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 67
                        self.match(JertlParser.T__1)
                        self.state = 68
                        localctx._key_value = self.key_value()
                        localctx.key_values.append(localctx._key_value) 
                    self.state = 73
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

                self.state = 76
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==2:
                    self.state = 74
                    self.match(JertlParser.T__1)
                    self.state = 75
                    self.kwargs()


                self.state = 78
                self.match(JertlParser.T__2)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 80
                self.match(JertlParser.T__0)
                self.state = 81
                self.match(JertlParser.T__2)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Key_valueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(JertlParser.STRING, 0)

        def structure(self):
            return self.getTypedRuleContext(JertlParser.StructureContext,0)


        def getRuleIndex(self):
            return JertlParser.RULE_key_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKey_value" ):
                listener.enterKey_value(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKey_value" ):
                listener.exitKey_value(self)




    def key_value(self):

        localctx = JertlParser.Key_valueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_key_value)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 84
            self.match(JertlParser.STRING)
            self.state = 85
            self.match(JertlParser.T__3)
            self.state = 86
            self.structure()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KwargsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variable(self):
            return self.getTypedRuleContext(JertlParser.VariableContext,0)


        def getRuleIndex(self):
            return JertlParser.RULE_kwargs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKwargs" ):
                listener.enterKwargs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKwargs" ):
                listener.exitKwargs(self)




    def kwargs(self):

        localctx = JertlParser.KwargsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_kwargs)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self.match(JertlParser.T__4)
            self.state = 89
            self.variable()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self._element = None # ElementContext
            self.elements = list() # of ElementContexts

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JertlParser.ElementContext)
            else:
                return self.getTypedRuleContext(JertlParser.ElementContext,i)


        def getRuleIndex(self):
            return JertlParser.RULE_array

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArray" ):
                listener.enterArray(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArray" ):
                listener.exitArray(self)




    def array(self):

        localctx = JertlParser.ArrayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_array)
        self._la = 0 # Token type
        try:
            self.state = 104
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 91
                self.match(JertlParser.T__5)
                self.state = 92
                localctx._element = self.element()
                localctx.elements.append(localctx._element)
                self.state = 97
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==2:
                    self.state = 93
                    self.match(JertlParser.T__1)
                    self.state = 94
                    localctx._element = self.element()
                    localctx.elements.append(localctx._element)
                    self.state = 99
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 100
                self.match(JertlParser.T__6)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 102
                self.match(JertlParser.T__5)
                self.state = 103
                self.match(JertlParser.T__6)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def structure(self):
            return self.getTypedRuleContext(JertlParser.StructureContext,0)


        def varargs(self):
            return self.getTypedRuleContext(JertlParser.VarargsContext,0)


        def getRuleIndex(self):
            return JertlParser.RULE_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElement" ):
                listener.enterElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElement" ):
                listener.exitElement(self)




    def element(self):

        localctx = JertlParser.ElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_element)
        try:
            self.state = 108
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 6, 10, 11, 12, 13, 16, 17, 18]:
                self.enterOuterAlt(localctx, 1)
                self.state = 106
                self.structure()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 2)
                self.state = 107
                self.varargs()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarargsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variable(self):
            return self.getTypedRuleContext(JertlParser.VariableContext,0)


        def getRuleIndex(self):
            return JertlParser.RULE_varargs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarargs" ):
                listener.enterVarargs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarargs" ):
                listener.exitVarargs(self)




    def varargs(self):

        localctx = JertlParser.VarargsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_varargs)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 110
            self.match(JertlParser.T__7)
            self.state = 111
            self.variable()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NULL(self):
            return self.getToken(JertlParser.NULL, 0)

        def TRUE(self):
            return self.getToken(JertlParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(JertlParser.FALSE, 0)

        def INTEGER(self):
            return self.getToken(JertlParser.INTEGER, 0)

        def FLOAT(self):
            return self.getToken(JertlParser.FLOAT, 0)

        def STRING(self):
            return self.getToken(JertlParser.STRING, 0)

        def getRuleIndex(self):
            return JertlParser.RULE_atom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom" ):
                listener.enterAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom" ):
                listener.exitAtom(self)




    def atom(self):

        localctx = JertlParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            _la = self._input.LA(1)
            if not(((_la) & ~0x3f) == 0 and ((1 << _la) & 408576) != 0):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(JertlParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return JertlParser.RULE_variable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariable" ):
                listener.enterVariable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariable" ):
                listener.exitVariable(self)




    def variable(self):

        localctx = JertlParser.VariableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_variable)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.match(JertlParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





