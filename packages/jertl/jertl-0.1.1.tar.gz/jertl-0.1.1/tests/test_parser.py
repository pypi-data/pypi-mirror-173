import pytest
from jertl.ast.builder import parse_string
from jertl.exceptions  import JertlSyntaxError

positive_tests = [['structure', '{"an": "object"}'],
                  ['structure', '["a", 4, "element", array]'],
                  ['structure', '"atom"'],
                  ['structure', 'variable'],
                  ['array',     '[1, 2, True]'],
                  ['array',     '[]'],
                  ['array',     '[1, "have a", *splat, "or", *two]'],
                  ['atom',      'null'],
                  ['atom',      'true'],
                  ['atom',      'false'],
                  ['atom',      '1'],
                  ['atom',      '3.14159'],
                  ['atom',      '"string"'],
                  ['obj',       '{"integer": 1, "list": [a, 4.4, *spread], **kw}'],
                  ['transform', '{"integer": 1, "list": [a, 4.4, *spread], **kw} --> True'],
                  ['matcher',   'thing ~ {"integer": 1, "list": [a, 4.4, *spread], **kw}'],
                  ['setter',    'result := {"integer": 1}'],
                  ['setter',    'result := {"integer": 1, "list": [a, 4.4, *spread], **kw}'],
                  ['collation', '''
                                    thing1 ~ {"integer": 1, "list": [_, 4.4, *spread], **kw}
                                    thing2 ~ thing1
                                    thing3 ~ [thing1, thing2]
                                '''],
                  ['rule_',     '''
                                    thing1 ~ {"integer": 1, "list": [a, 4.4, *spread], **kw}
                                    thing2 ~ thing1
                                    thing3 ~ [thing1, thing2]
                                  -->
                                    thong1 := {"integer": 2, "list": [thing3, 4.4, *spread], **kw}
                                ''']]

@pytest.mark.parametrize('rule,source', positive_tests)
def test_parse(rule, source):
    parse_string(source, rule)

def test_failure():
    with pytest.raises(JertlSyntaxError):
        parse_string('[$internal_variable_name]', 'structure')

def test_null_collation():
    parse_string('', 'collation')

def test_null_rule():
    parse_string('-->', 'rule_')
