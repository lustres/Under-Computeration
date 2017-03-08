from FizzBuzz import *


def test_number():
    assert integer(ZERO) == 0
    assert integer(ONE) == 1
    assert integer(TWO) == 2
    assert integer(THREE) == 3
    assert integer(FIVE) == 5
    assert integer(FIFTEEN) == 15
    # assert integer(HUNDRED) == 100
