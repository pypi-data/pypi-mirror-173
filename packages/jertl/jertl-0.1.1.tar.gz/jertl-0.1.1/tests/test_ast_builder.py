import pytest
from jertl.ast.builder        import ast_for_string
from jertl.ast.representation import Variable, VarArgs, KWArgs
from jertl.ast.representation import Matcher,  Setter,  Transform, Rule

tests = [['structure', '{"an": "object"}',
                        {'an': 'object'}],

         ['structure', '["a", 4, "element", array]',
                        ['a', 4, 'element', Variable('array')]],

         ['structure', '"atom"',
                        'atom'],

         ['structure', 'variable',
                        Variable('variable')],

         ['array',     '[1, 2, true]',
                        [1, 2, True]],

         ['array',     '[]',
                        []],

         ['array',     '[1, "have a", *splat,                     "or", *two]',
                        [1, 'have a', VarArgs(Variable('splat')), 'or', VarArgs(Variable('two'))]],

         ['atom',      'null',
                        None],

         ['atom',      'true',
                        True],

         ['atom',      'false',
                        False],

         ['atom',      '1',
                        1],

         ['atom',      '3.14159',
                        3.14159],

         ['atom',      '"string"',
                        'string'],

         ['obj',       '{"integer": 1, "list": [a,             4.4, *spread],                  **kw}',
                        {'integer': 1,
                         'list': [Variable('a'), 4.4, VarArgs(variable=Variable('spread'))],
                         KWArgs(): Variable('kw')}],

         ['transform', '{"integer": 1, "list": [a, 4.4, *spread], **kw} --> true',
                        Transform(input={'integer': 1,
                                         'list': [Variable('a'), 4.4, VarArgs(variable=Variable('spread'))],
                                         KWArgs(): Variable('kw')},
                                  output=True)],

         ['matcher',   'thing ~ {"integer": 1, "list": [a, 4.4, *spread], **kw}',
                        Matcher(variable=Variable('thing'),
                                structure={'integer': 1,
                                           'list': [Variable('a'), 4.4, VarArgs(variable=Variable('spread'))],
                                           KWArgs(): Variable('kw')})],

         ['setter',    'result := {"integer": 1}',
                        Setter(variable=Variable('result'), structure={'integer': 1})],

         ['setter',    'result := {"integer": 1, "list": [a, 4.4, *spread], **kw}',
                        Setter(variable=Variable('result'),
                               structure={'integer': 1,
                                          'list':    [Variable('a'),
                                                      4.4,
                                                      VarArgs(variable=Variable('spread'))],
                                          KWArgs():  Variable('kw')})],

         ['collation', '''
                         thing1 ~ {"integer": 1, "list": [x, 4.4, *spread], **kw}
                         thing2 ~ thing1
                         thing3 ~ [thing1, thing2]
                     ''',
                     [Matcher(variable=Variable('thing1'),
                              structure={'integer': 1,
                                         'list': [Variable('x'), 4.4, VarArgs(variable=Variable('spread'))],
                                          KWArgs():  Variable('kw')}),
                      Matcher(variable=Variable('thing2'), structure=Variable('thing1')),
                      Matcher(variable=Variable('thing3'), structure=[Variable('thing1'), Variable('thing2')])]],

         ['rule_',     '''
                           thing1 ~ {"integer": 1, "list": [a, 4.4, *spread], **kw}
                           thing2 ~ thing1
                           thing3 ~ [thing1, thing2]
                         -->
                           thong1 := {"integer": 2, "list": [thing3, 4.4, *spread], **kw}
                       ''',
                     Rule(matchers=[Matcher(variable=Variable('thing1'),
                                            structure={KWArgs(): Variable('kw'),
                                                        'integer': 1,
                                                        'list': [Variable('a'), 4.4, VarArgs(variable=Variable('spread'))]}),
                                    Matcher(variable=Variable('thing2'), structure=Variable('thing1')),
                                    Matcher(variable=Variable('thing3'), structure=[Variable('thing1'), Variable('thing2')])],
                          setters=[Setter(variable=Variable('thong1'),
                                          structure={'integer': 2,
                                                     'list': [Variable('thing3'),
                                                              4.4,
                                                              VarArgs(variable=Variable('spread'))],
                                                     KWArgs(): Variable('kw')})])],

         ['rule_',     '-->',  Rule(matchers=[], setters=[])],
         ['collation', '',     []]]

@pytest.mark.parametrize('rule,source,result', tests)
def test_ast_for_string(rule, source, result):
    ast = ast_for_string(source, rule)
    assert ast == result
