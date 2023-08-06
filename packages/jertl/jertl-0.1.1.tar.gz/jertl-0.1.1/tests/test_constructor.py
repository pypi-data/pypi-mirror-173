import pytest

from jertl.ast.builder        import ast_for_string
from jertl.engine.construct   import construct, ensure_purity


tests = [['x',
          {'x': 100},
          100],

         ['[x, y, "z"]',
           {'x': True, 'y': None},
           [True, None, 'z']],

         ['[1, 2, *splat]',
           {'splat': [3, 4, 5]},
           [1, 2, 3, 4, 5]],

         ['[1, 2.2, true, null, "String"]',
           {},
           [1, 2.2, True, None, 'String']],

         ['{"1": 1, "2": 2, **splot}',
          {'splot': {"3": 3, "4": 4, "5": 5}},
          {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5}],

         ['{"1": 1, "list": [1, {"inner": x}, *splat, y], **splot}',
            {'x': True, 'y': None, 'splat': [3, 4, 5], 'splot': {"3": 3, "4": 4, "5": 5}},
            {'1': 1, 'list': [1, {'inner': True}, 3, 4, 5, None], '3': 3, '4': 4, '5': 5}]]

@pytest.mark.parametrize('pattern,bindings,result', tests)
def test_ast_for_string(pattern, bindings, result):
    structure = ast_for_string(pattern, 'structure')
    constructed = construct(structure, bindings)
    assert constructed == result
    ensure_purity(constructed)
