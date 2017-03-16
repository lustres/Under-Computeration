from calculus import *


def test_grammar():
    one = Function('p', Function('x', Call(Variable('p'), Variable('x'))))
    assert repr(one) == 'lambda p: lambda x: p(x)'


def test_grammar_2():
    increment = Function('n', Function('p', Function('x',
                                                     Call(
                                                         Variable('p'),
                                                         Call(
                                                             Call(
                                                                 Variable('n'), Variable('p')),
                                                             Variable('x'))))))
    assert repr(increment) == 'lambda n: lambda p: lambda x: p(n(p)(x))'

def test_grammar_3():
    add = Function('m', Function('n', Function('f', Function('x',
                                                             Call(
                                                                 Call(
                                                                     Variable('m'), Variable('f')),
                                                                 Call(
                                                                     Call(
                                                                         Variable('n'), Variable('f')),
                                                                     Variable('x')))))))
    assert repr(add) == 'lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))'
