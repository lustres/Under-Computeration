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
