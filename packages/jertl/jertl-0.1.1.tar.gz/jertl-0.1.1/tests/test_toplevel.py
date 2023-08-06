import jertl
from   jertl.engine.construct import ensure_purity

def test_match_all():
    matches = list(jertl.match_all('[*x, [y, [*z, *z], y], *x]', [1, [2, [3, 3], 2] ,1]))
    assert len(matches) == 1
    assert matches[0].bindings['x'] == [1]
    assert matches[0].bindings['y'] ==  2
    assert matches[0].bindings['z'] == [3]

def test_compiled_match():
    matcher = jertl.compile_match('[*before, x, *after]')
    for i, match in enumerate(matcher.match_all(list(range(3)))):
        assert match.bindings['before'] == list(range(i))
        assert match.bindings['x']      == i
        assert match.bindings['after']  == list(range(i+1, 3))

        ensure_purity(match.matched)

def test_fill():
    assert jertl.fill('[a, b, c]', a=True, b=None, c='a string') == [True, None, 'a string']

def test_compiled_fill():
    filler = jertl.compile_fill('[a, b]')

    for pair in [[1,2], [7,9]]:
      assert filler.fill(a=pair[0], b=pair[1]) == pair

def test_collate_all():
    collations = list(jertl.collate_all('''
                                      employee   ~ {"Name": "Ray", "Supervisor": supervisor_id}
                                      supervisor ~ {"EmployeeId": supervisor_id}
                                      ''',
                                      employee={'Name': 'Ray', 'Supervisor': 666},
                                      supervisor={'EmployeeId': 666}))
    assert len(collations) == 1
    assert collations[0].bindings == {'employee': {'Name': 'Ray', 'Supervisor': 666}, 'supervisor': {'EmployeeId': 666}, 'supervisor_id': 666}

def test_compiled_collate():
    collator = jertl.compile_collate('''
                                   a ~ [*_, n, *_]
                                   b ~ [*_, n, *_]
                                   ''')
    collations = list(collator.collate_all(a=[1, 2, 3, 4], b=[4, 2]))
    assert len(collations) == 2
    assert collations[0].bindings['n'] == 2
    assert collations[1].bindings['n'] == 4

def test_transform_all():
    transforms = list(jertl.transform_all('[*a, x, b, y, *c] --> [y, x]', [1,2,3,4,5]))
    assert len(transforms) == 3
    assert transforms[0].filled == [3, 1]
    assert transforms[1].filled == [4, 2]
    assert transforms[2].filled == [5, 3]

def test_compiled_inference():
    rule = jertl.compile_rule('''
							a ~ [*_1, n, x, *_2]
							b ~ [*_3, n, y, *_4]
						-->
							c := [n, [x, y]]
					    ''')

    inferences = list(rule.infer_all(a=[1, 2, 3, 4, 12], b=[4, 2, 7]))
    assert len(inferences) == 2
    assert inferences[0].fills == {'c': [2, [3, 7]]}
    assert inferences[1].fills == {'c': [4, [12, 2]]}
