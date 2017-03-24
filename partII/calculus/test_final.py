from fundation import *

def ans(term):
    return str(reduce(term))


def call(self, *args, **kwargs):
    return Call(self, args[0])


Term.__call__ = call


def test_boolean():
    assert ans(IF(TRUE)(Variable('happy'))(Variable('sad'))) == 'happy'
    assert ans(IF(FALSE)(Variable('happy'))(Variable('sad'))) == 'sad'


def test_boolean_AND():
    assert ans(AND(TRUE)(TRUE)) == ans(TRUE)
    assert ans(AND(TRUE)(FALSE)) == ans(FALSE)
    assert ans(AND(FALSE)(TRUE)) == ans(FALSE)
    assert ans(AND(FALSE)(FALSE)) == ans(FALSE)


def test_boolean_OR():
    assert ans(OR(TRUE)(TRUE)) == ans(TRUE)
    assert ans(OR(TRUE)(FALSE)) == ans(TRUE)
    assert ans(OR(FALSE)(TRUE)) == ans(TRUE)
    assert ans(OR(FALSE)(FALSE)) == ans(FALSE)


def test_boolean_NOT():
    assert ans(NOT(TRUE)) == ans(FALSE)
    assert ans(NOT(FALSE)) == ans(TRUE)


def test_predicate():
    assert ans(IS_ZERO(ZERO)) == ans(TRUE)
    assert ans(IS_ZERO(THREE)) == ans(FALSE)
    assert ans((IS_ZERO(FIFTEEN))) == ans(FALSE)


def test_pair():
    pair = PAIR(THREE)(FIVE)
    assert ans(LEFT(pair)) == ans(THREE)
    assert ans(RIGHT(pair)) == ans(FIVE)


def test_pair_2():
    pair = PAIR(ZERO)(FIFTEEN)
    assert ans(LEFT(pair)) == ans(ZERO)
    assert ans(RIGHT(pair)) == ans(FIFTEEN)


def test_increment():
    assert ans(INCREMENT(ZERO)) == ans(ONE)
    assert ans((INCREMENT(TWO))) == ans(THREE)
    # assert ans(INCREMENT(FIFTEEN)) == ans(ADD(FIFTEEN)(ONE))
    assert ans(INCREMENT(FIFTEEN)(Variable('one'))) == ans(ADD(FIFTEEN)(ONE)(Variable('one')))

def test_slide():
    NEXT_PAIR = SLIDE(PAIR(ZERO)(ZERO))
    assert ans(LEFT(NEXT_PAIR)) == ans(ZERO)
    assert ans(RIGHT(NEXT_PAIR)) == ans(ONE)

    NEXT_PAIR = SLIDE(NEXT_PAIR)
    assert ans(LEFT(NEXT_PAIR)) == ans(ONE)
    assert ans((RIGHT(NEXT_PAIR))) == ans(TWO)


def test_decrement():
    assert ans(DECREMENT(ONE)) == ans(ZERO)
    assert ans(DECREMENT(TWO)) == ans(ONE)
    assert ans(DECREMENT(THREE)) == ans(TWO)


def test_math():
    assert ans(ADD(TWO)(THREE)) == ans(alpha(FIVE, Variable('f')))
    assert ans(SUB(FIVE)(THREE)) == ans(alpha(TWO, Variable('p')))
    assert ans(MULTI(THREE)(FIVE)) == ans(alpha(FIFTEEN, Variable('f')))
    assert ans(DIV(TEN)(THREE)) == ans(THREE)
    # assert ans(POWER(THREE)(THREE)) == ans(MULTI(POWER(THREE)(TWO))(THREE))
    assert ans(POWER(THREE)(THREE)(Variable('one'))) == ans(MULTI(POWER(THREE)(TWO))(THREE)(Variable('one')))

def test_less_or_equal():
    assert ans(LESS_OR_EQUAL(ONE)(TWO)) == ans(TRUE)
    assert ans(LESS_OR_EQUAL(FIVE)(THREE)) == ans(FALSE)
    assert ans(LESS_OR_EQUAL(FIFTEEN)(FIFTEEN)) == ans(TRUE)


def test_mod():
    assert ans(MOD(FIFTEEN)(FIVE)) == ans(ZERO)
    assert ans(MOD(FIFTEEN)(THREE)) == ans(ZERO)
    assert ans(MOD(FIFTEEN)(TWO)) == ans(ONE)


def test_array():
    L = UNSHIFT(
        UNSHIFT(
            UNSHIFT(EMPTY)(THREE)
        )(TWO)
    )(ONE)

    assert ans(IS_EMPTY(L)) == ans(FALSE)
    assert ans(FIRST(L)) == ans(ONE)
    assert ans(FIRST(REST(L))) == ans(TWO)
    assert ans(FIRST(REST(REST(L)))) == ans(THREE)
    assert ans(IS_EMPTY(FIRST(REST(REST(REST))))) == ans(TRUE)

#
# def test_array_2():
#     L = UNSHIFT(
#         UNSHIFT(
#             UNSHIFT(EMPTY)(THREE)
#         )(TWO)
#     )(ONE)
#
#     assert array(EMPTY) == []
#     assert list(map(integer, array(L))) == [1,2,3]
#
#
# def test_range():
#     assert list(map(integer, array(RANGE(ONE)(ONE)))) == [1]
#     assert list(map(integer, array(RANGE(ZERO)(FIFTEEN)))) == list(range(0, 15+1))
#     assert list(map(integer, array(RANGE(ONE)(POWER(MULTI(TWO)(FIVE))(TWO))))) == list(range(1, (2 * 5) ** 2 + 1))
#

def test_infinity():
    assert ans(FIRST(INFINITY)) == ans(ZERO)
    assert ans(FIRST(REST(INFINITY))) == ans(ZERO)
    assert ans(FIRST(REST(REST(INFINITY)))) == ans(ZERO)

#
# def test_infinity_2():
#     assert list(map(integer, array(INFINITY, 5))) == [0 for i in range(5)]
#     assert list(map(integer, array(INFINITY, 10))) == [0 for i in range(10)]
#     assert list(map(integer, array(INFINITY, 20))) == [0 for i in range(20)]
#
#
# def test_progress():
#     assert list(map(integer, array(PROGRESS(ZERO), 5))) == [i for i in range(5)]
#     assert list(map(integer, array(PROGRESS(FIFTEEN), 20))) == [i for i in range(15, 15 + 20)]
#
#
# def test_multiple():
#     assert list(map(integer, array(MULTIPLE(TWO),   10))) == [i * 2 for i in range(1, 10 + 1)]
#     assert list(map(integer, array(MULTIPLE(THREE), 10))) == [i * 3 for i in range(1, 10 + 1)]
#     assert list(map(integer, array(MULTIPLE(FIVE),  20))) == [i * 5 for i in range(1, 20 + 1)]
#
#
# def test_generator():
#     assert list(map(integer, array(GENERATOR(TWO)(ADD(TWO)), 10))) == [i * 2 for i in range(1, 10 + 1)]
#     assert list(map(integer, array(GENERATOR(FIVE)(ADD(FIVE)), 20))) == [i * 5 for i in range(1, 20 + 1)]
#

def test_fold():
    assert ans(FOLD(RANGE(ONE)(FIVE))(ZERO)(ADD)) == ans(alpha(FIFTEEN, Variable('f')))
    # assert ans(FOLD(RANGE(ONE)(FIVE))(ONE)(MULTI)) == ans(alpha(MULTI(MULTI(POWER(TWO)(THREE))(THREE))(FIVE), Variable('f')))
    assert ans(FOLD(RANGE(ONE)(FIVE))(ONE)(MULTI)(Variable('one'))) == ans(MULTI(MULTI(POWER(TWO)(THREE))(THREE))(FIVE)(Variable('one')))
#
# def test_map():
#     assert list(map(integer, array(MAP(RANGE(ONE)(THREE))(INCREMENT)))) == [2, 3, 4]
#
#
# def test_merge():
#     assert list(map(integer,  array(MERGE(PROGRESS(ZERO))(PROGRESS(ZERO))(ADD), 10))) == [i * 2 for i in range(10)]
