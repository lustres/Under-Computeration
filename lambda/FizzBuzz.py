ZERO    = lambda p: lambda x: x
ONE     = lambda p: lambda x: p(x)
TWO     = lambda p: lambda x: p(p(x))
THREE   = lambda p: lambda x: p(p(p(x)))
FIVE    = lambda p: lambda x: p(p(p(p(p(x)))))
FIFTEEN = lambda p: lambda x: p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(x)))))))))))))))
## parser will stack overflow :(
# HUNDRED = lambda p: lambda x: p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(
#                               p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(
#                               p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(
#                               p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(
#                               p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(
#                                                  x
#                               ))))))))))))))))))))))))))))))))))))))))
#                               ))))))))))))))))))))))))))))))))))))))))
#                               ))))))))))))))))))))


def integer(l):
    return l(lambda n: n + 1)(0)


TRUE  = lambda x: lambda y: x
FALSE = lambda x: lambda y: y


IF = lambda b: b


def boolean(l):
    return IF(l)(True)(False)


IS_ZERO = lambda l: l(lambda n: FALSE)(TRUE)


PAIR  = lambda x: lambda y: lambda f: f(x)(y)
LEFT  = lambda f: f(lambda x: lambda y: x)
RIGHT = lambda f: f(lambda x: lambda y: y)


INCREMENT = lambda n: lambda p: lambda x: p(n(p)(x))
