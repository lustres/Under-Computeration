from terms import *


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


SLIDE = lambda p: PAIR(RIGHT(p))(INCREMENT(RIGHT(p)))


DECREMENT = lambda n: LEFT(n(SLIDE)(PAIR(ZERO)(ZERO)))

# A = λm.λn.m(...m(m(n))...)
# B = λx.λy.x(...x(x(y))...)
# ADD = λA.λB.λp.λq.p(...p(p(q))...)
# so we should let:
#     m = λp
#     n = B λp λq
# ADD = λA.λB.λp.λq.A p (B p q)
ADD = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))
# ADD = lambda m: lambda n: n(INCREMENT)(m)

SUB = lambda m: lambda n: n(DECREMENT)(m)

# A = λm.λn.m(...m(m(n))...)
# B = λx.λy.x(...x(x(y))...)
# MULTI = λA.λB.λp.λq.p(...p(p(q))...)
# so we should let:
#     m = B λp
#     n = λq
# MULTI = λA.λB.λp.λq.A (B p) q
# MULTI = λA.λB.λp.λq.A (B p) q
# apply β-reduction (on q)
# MULTI = λA.λB.λp.A (B p)
MULTI = lambda m: lambda n: lambda f: m(n(f))
# MULTI = lambda m: lambda n: n(ADD(m))(ZERO)

# A = λm.λn.m(...m(m(n))...)
# B = λx.λy.x(...x(x(y))...)
# POWER = λA.λB.λp.λq.A(...A(p)...) q
#     m = A
#     n = p
# POWER = λA.λB.λp.λq.B A p q
# apply β-reduction (on q)
# POWER = λA.λB.λp.B A p
# apply β-reduction (on p)
# POWER = λA.λB.B A
POWER = lambda b: lambda e: e(b)
# POWER = lambda m: lambda n: n(MULTI(m))(ONE)


LESS_OR_EQUAL = lambda m: lambda n: IS_ZERO(SUB(m)(n))


# MOD = lambda m: lambda n: IF(LESS_OR_EQUAL(n)(m))(MOD(SUB(m)(n))(n))(m)
# MOD = lambda m: lambda n: IF(LESS_OR_EQUAL(n)(m))(lambda x: MOD(SUB(m)(n))(n)(x))(m)
# MOD = Y(lambda f: lambda m: lambda n: IF(LESS_OR_EQUAL(n)(m))(lambda x: f(SUB(m)(n))(n)(x))(m))
MOD = Z(lambda f: lambda m: lambda n: IF(LESS_OR_EQUAL(n)(m))(lambda x: f(SUB(m)(n))(n)(x))(m))
