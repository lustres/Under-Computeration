from calculus import *


one = Function('p', Function('x', Call(Variable('p'), Variable('x'))))

increment = Function('n', Function('p', Function('x',
                                                 Call(
                                                     Variable('p'),
                                                     Call(
                                                         Call(
                                                             Variable('n'), Variable('p')),
                                                         Variable('x'))))))

add = Function('m', Function('n', Function('f', Function('x',
                                                         Call(
                                                             Call(
                                                                 Variable('m'), Variable('f')),
                                                             Call(
                                                                 Call(
                                                                     Variable('n'), Variable('f')),
                                                                 Variable('x')))))))
def test_grammar():
    assert repr(one) == 'lambda p: lambda x: p(x)'


def test_grammar_2():
    assert repr(increment) == 'lambda n: lambda p: lambda x: p(n(p)(x))'

def test_grammar_3():
    assert repr(add) == 'lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))'


def test_semantic_replace():
    e = Variable('x')
    assert repr(e.replace('x', Function('y', Variable('y')))) == 'lambda y: y'
    assert repr(e.replace('z', Function('y', Variable('y')))) == repr(e)


def test_semantic_replace_2():
    e = Call(
            Call(
                Call(Variable('a'), Variable('b')),
                Variable('c')),
            Variable('b'))
    assert repr(e.replace('a', Variable('x'))) == 'x(b)(c)(b)'
    assert repr(e.replace('b', Function('x', Variable('x')))) == 'a(lambda x: x)(c)(lambda x: x)'


def test_semantic_replace_3():
    e = Call(
            Call(
                Variable('x'), Variable('y')),
            Function('y',
                     Call(Variable('y'), Variable('x'))))
    assert repr(e.replace('x', Variable('z'))) == 'z(y)(lambda y: y(z))'
    assert repr(e.replace('y', Variable('z'))) == 'x(z)(lambda y: y(x))'


def test_semantic_replace_4():
    """
    This function shows the bug in replace method.
    """
    e = Function('x',
                 Call(Variable('x'), Variable('y')))
    replacement = Call(Variable('z'), Variable('x'))
    assert repr(e.replace('y', replacement)) == 'lambda x: x(z(x))'


def test_semantic_call():
    f = Function('x', Function('y', Call(Variable('x'), Variable('y'))))
    arg = Function('z', Variable('z'))
    assert repr(f.call(arg)) == 'lambda y: lambda z: z(y)'


def test_semantic_reduce():
    e = Call(Call(add, one), one)
    inc = Variable('inc')
    zero = Variable('zero')
    e = Call(Call(e, inc), zero)
    while is_reducible(e):
        e = e.reduce()
    assert repr(e) == 'inc(inc(zero))'
