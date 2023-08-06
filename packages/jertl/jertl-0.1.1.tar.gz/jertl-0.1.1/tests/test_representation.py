from jertl.ast.representation import Variable

# Variables

def test_equality():
    assert Variable('x') == Variable('x')

def test_inequality():
    assert Variable('x') != Variable('y')

def test_uniqueness_of_anonymous_variables():
    assert Variable('_') != Variable('_')

def test_representation_of_anonymous_variables():
    assert repr(Variable('_')) == '_'

def test_identifier_of_anonymous_variables():
    anonymous_variable = Variable('_')
    assert anonymous_variable.identifier != '_'
    assert anonymous_variable.identifier.startswith('$')
