from FizzBuzz import *


def test_number():
    assert integer(ZERO) == 0
    assert integer(ONE) == 1
    assert integer(TWO) == 2
    assert integer(THREE) == 3
    assert integer(FIVE) == 5
    assert integer(FIFTEEN) == 15
    # assert integer(HUNDRED) == 100


def test_boolean():
    assert IF(TRUE)('happy')('sad') == 'happy'
    assert IF(FALSE)('happy')('sad') == 'sad'


def test_boolean_AND():
    assert boolean(AND(TRUE)(TRUE)) == True
    assert boolean(AND(TRUE)(FALSE)) == False
    assert boolean(AND(FALSE)(TRUE)) == False
    assert boolean(AND(FALSE)(FALSE)) == False


def test_boolean_OR():
    assert boolean(OR(TRUE)(TRUE)) == True
    assert boolean(OR(TRUE)(FALSE)) == True
    assert boolean(OR(FALSE)(TRUE)) == True
    assert boolean(OR(FALSE)(FALSE)) == False


def test_boolean_NOT():
    assert boolean(NOT(TRUE)) == False
    assert boolean(NOT(FALSE)) == True


def test_predicate():
    assert boolean(IS_ZERO(ZERO)) == True
    assert boolean(IS_ZERO(THREE)) == False
    assert boolean((IS_ZERO(FIFTEEN))) == False


def test_pair():
    pair = PAIR(THREE)(FIVE)
    assert integer(LEFT(pair)) == 3
    assert integer(RIGHT(pair)) == 5


def test_pair_2():
    pair = PAIR(ZERO)(FIFTEEN)
    assert integer(LEFT(pair)) == 0
    assert integer(RIGHT(pair)) == 15


def test_increment():
    assert integer(INCREMENT(ZERO)) == 1
    assert integer((INCREMENT(TWO))) == 3
    assert integer(INCREMENT(FIFTEEN)) == 16


def test_slide():
    NEXT_PAIR = SLIDE(PAIR(ZERO)(ZERO))
    assert integer(LEFT(NEXT_PAIR)) == 0
    assert integer(RIGHT(NEXT_PAIR)) == 1

    NEXT_PAIR = SLIDE(NEXT_PAIR)
    assert integer(LEFT(NEXT_PAIR)) == 1
    assert integer((RIGHT(NEXT_PAIR))) == 2


def test_decrement():
    assert integer(DECREMENT(ONE)) == 0
    assert integer(DECREMENT(TWO)) == 1
    assert integer(DECREMENT(THREE)) == 2


def test_math():
    assert integer(ADD(TWO)(THREE)) == 5
    assert integer(SUB(FIVE)(THREE)) == 2
    assert integer(MULTI(THREE)(FIVE)) == 15
    assert integer(POWER(THREE)(FIVE)) == pow(3, 5)


def test_less_or_equal():
    assert boolean(LESS_OR_EQUAL(ONE)(TWO)) == True
    assert boolean(LESS_OR_EQUAL(FIVE)(THREE)) == False
    assert boolean(LESS_OR_EQUAL(FIFTEEN)(FIFTEEN)) == True


def test_mod():
    assert integer(MOD(FIFTEEN)(FIVE)) == 0
    assert integer(MOD(FIFTEEN)(THREE)) == 0
    assert integer(MOD(FIFTEEN)(TWO)) == 1


def test_array():
    L = UNSHIFT(
        UNSHIFT(
            UNSHIFT(EMPTY)(THREE)
        )(TWO)
    )(ONE)

    assert boolean(IS_EMPTY(L)) == False
    assert integer(FIRST(L)) == 1
    assert integer(FIRST(REST(L))) == 2
    assert integer(FIRST(REST(REST(L)))) == 3
    assert boolean(IS_EMPTY(FIRST(REST(REST(REST))))) == True


def test_array_2():
    L = UNSHIFT(
        UNSHIFT(
            UNSHIFT(EMPTY)(THREE)
        )(TWO)
    )(ONE)

    assert array(EMPTY) == []
    assert list(map(integer, array(L))) == [1,2,3]


def test_range():
    assert list(map(integer, array(RANGE(ONE)(ONE)))) == [1]
    assert list(map(integer, array(RANGE(ZERO)(FIFTEEN)))) == list(range(0, 15+1))
    assert list(map(integer, array(RANGE(ONE)(POWER(MULTI(TWO)(FIVE))(TWO))))) == list(range(1, (2 * 5) ** 2 + 1))


def test_fold():
    assert integer(FOLD(RANGE(ONE)(FIVE))(ZERO)(ADD)) == 15
    assert integer(FOLD(RANGE(ONE)(FIVE))(ONE)(MULTI)) == 120