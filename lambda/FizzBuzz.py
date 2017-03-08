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
