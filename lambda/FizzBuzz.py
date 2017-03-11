from terms import *


ZERO    = lambda p: lambda x: x
ONE     = lambda p: lambda x: p(x)
TWO     = lambda p: lambda x: p(p(x))
THREE   = lambda p: lambda x: p(p(p(x)))
FOUR    = lambda p: lambda x: p(p(p(p(x))))
FIVE    = lambda p: lambda x: p(p(p(p(p(x)))))
TEN     = lambda p: lambda x: p(p(p(p(p(p(p(p(p(p(x))))))))))
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


TRUE  = lambda x: lambda y: x
FALSE = lambda x: lambda y: y

IF = lambda b: b

# AND = λx.λy.λa.λb.x (y a b) b
# OR  = λx.λy.λa.λb.x b (y a b)
# NOT = λx.λa.λb.x b a
AND = lambda x: lambda y: x(y)(x)
OR  = lambda x: lambda y: x(x)(y)
NOT = lambda x: x(FALSE)(TRUE)

IS_ZERO = lambda l: l(lambda n: FALSE)(TRUE)
LESS_OR_EQUAL = lambda m: lambda n: IS_ZERO(SUB(m)(n))


INCREMENT = lambda n: lambda p: lambda x: p(n(p)(x))
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

# def div(m, n):
#     if n <= m:
#         return div(m - n, n) + 1
#     else:
#         return 0
# DIV = lambda m: lambda n: IF(LESS_OR_EQUAL(n)(m))(INCREMENT(DIV(SUB(m)(n))(n)))(ZERO)
# DIV = lambda m: lambda n: IF(LESS_OR_EQUAL(n)(m))(lambda x: INCREMENT(DIV(SUB(m)(n))(n))(x))(ZERO)
DIV = Z(lambda f: lambda m: lambda n: IF(LESS_OR_EQUAL(n)(m))(lambda x: INCREMENT(f(SUB(m)(n))(n))(x))(ZERO))

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


# MOD = lambda m: lambda n: IF(LESS_OR_EQUAL(n)(m))(MOD(SUB(m)(n))(n))(m)
# MOD = lambda m: lambda n: IF(LESS_OR_EQUAL(n)(m))(lambda x: MOD(SUB(m)(n))(n)(x))(m)
# let G = lambda f: lambda m: lambda n: IF(LESS_OR_EQUAL(n)(m))(lambda x: f(SUB(m)(n))(n)(x))(m)
# => G f m n = f m n = MOD m n
# => G f = f = MOD
# => fix G = f = MOD
# Y G = Y (Y G)
# => Y G = fix G = f = MOD
# => MOD = Y G
# use lazy combinator Z to avoid strict evaluate
# MOD = Z G
MOD = Z(lambda f: lambda m: lambda n: IF(LESS_OR_EQUAL(n)(m))(lambda x: f(SUB(m)(n))(n)(x))(m))


PAIR  = lambda x: lambda y: lambda f: f(x)(y)
LEFT  = lambda f: f(TRUE)
RIGHT = lambda f: f(FALSE)
# LEFT  = lambda f: f(lambda x: lambda y: x)
# RIGHT = lambda f: f(lambda x: lambda y: y)


# ARRAY = (F, (1, (F, (2, (F, (3, (T, T)))))))
EMPTY    = PAIR(TRUE)(TRUE)
IS_EMPTY = LEFT
UNSHIFT  = lambda l: lambda x: PAIR(FALSE)(PAIR(x)(l))
PUSH = lambda l: lambda x: FOLD(l)(UNSHIFT(EMPTY)(x))(UNSHIFT)
FIRST = lambda l: LEFT(RIGHT(l))
REST  = lambda l: RIGHT(RIGHT(l))

SLIDE = lambda p: PAIR(RIGHT(p))(INCREMENT(RIGHT(p)))

# def range(m, n):
#     if m <= n:
#         return [m] + range(m+1, n)
#     else:
#         return []
# RANGE = lambda m: lambda n: IF(LESS_OR_EQUAL(m)(n))(UNSHIFT(RANGE(INCREMENT(m))(n))(m))(EMPTY)
# RANGE = lambda m: lambda n: IF(LESS_OR_EQUAL(m)(n))(lambda x: UNSHIFT(RANGE(INCREMENT(m))(n))(m)(x))(EMPTY)
RANGE = Z(lambda f: lambda m: lambda n: IF(LESS_OR_EQUAL(m)(n))(lambda x: UNSHIFT(f(INCREMENT(m))(n))(m)(x))(EMPTY))


# INFINITY = UNSHIFT(INFINITY)(ZERO)
INFINITY = Z(lambda f: UNSHIFT(f)(ZERO))


# def fold(l, acc, func):
#     if l:
#         return func(fold(l[1:], acc, func), l[0])
#     else:
#         return acc
# FOLD = lambda l: lambda x: lambda g: IF(IS_EMPTY(l))(x)(g(FOLD(REST(l))(x)(g))(FIRST(l)))
# FOLD = lambda l: lambda x: lambda g: IF(IS_EMPTY(l))(x)(lambda y: g(FOLD(REST(l))(x)(g))(FIRST(l))(y))
FOLD = Z(lambda f: lambda l: lambda x: lambda g: IF(IS_EMPTY(l))(x)(lambda y: g(f(REST(l))(x)(g))(FIRST(l))(y)))

# def map(l, func):
#     return fold(l, [], lambda array: lambda x: array.unshift(func(x)))
MAP = lambda k: lambda f: FOLD(k)(EMPTY)(lambda l: lambda x: UNSHIFT(l)(f(x)))


FIZZ     = UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(EMPTY)(ADD(TEN)(FOUR)))(ADD(TEN)(FOUR)))(ADD(TEN)(TWO)))(ADD(TEN)(ONE))
BUZZ     = UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(EMPTY)(ADD(TEN)(FOUR)))(ADD(TEN)(FOUR)))(ADD(TEN)(THREE)))(ADD(TEN)(ZERO))
FIZZBUZZ = UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(BUZZ)(ADD(TEN)(FOUR)))(ADD(TEN)(FOUR)))(ADD(TEN)(TWO)))(ADD(TEN)(ONE))


# def digits(n):
#     def previous():
#         if n <= 10-1:
#             return []
#         else:
#             return digits(n // 10)
#
#     # return previous().append(n % 10) array.append does not return
#     return previous() + [n % 10]
# DIGITS = lambda n: PUSH(IF(LESS_OR_EQUAL(n)(SUB(TEN)(ONE)))(EMPTY)(DIGITS(DIV(n)(TEN))))(MOD(n)(TEN))
# DIGITS = lambda n: PUSH(IF(LESS_OR_EQUAL(n)(SUB(TEN)(ONE)))(EMPTY)(lambda x: DIGITS(DIV(n)(TEN)))(x))(MOD(n)(TEN))
DIGITS = Z(lambda f: lambda n: PUSH(IF(LESS_OR_EQUAL(n)(SUB(TEN)(ONE)))(EMPTY)(lambda x: DIGITS(DIV(n)(TEN))(x)))(MOD(n)(TEN)))


def integer(l):
    return l(lambda n: n + 1)(0)


def boolean(l):
    return IF(l)(True)(False)


def array(l, count = None):
    a = []
    while not boolean(IS_EMPTY(l)) and count is not 0:
        a.append(FIRST(l))
        l = REST(l)
        if count is not None:
            count = count - 1
    return a


def character(c):
    return "0123456789BFiuz"[integer(c)]


def string(s):
    return "".join(map(character, array(s)))
