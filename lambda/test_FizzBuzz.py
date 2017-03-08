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
