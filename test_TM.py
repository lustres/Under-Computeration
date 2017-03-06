from TM import *
from base import RuleBook


def test_TM_1():
    rule = TMRule(1, '0', 2, '1', Direction.right)
    print(rule)
    assert rule.is_applied(TMConfig(1, Tape([], '0', []))) == True
    assert rule.is_applied(TMConfig(1, Tape([], '1', []))) == False
    assert rule.is_applied(TMConfig(2, Tape([], '0', []))) == False


def test_TM_2():
    tape = Tape.make('1011')
    rulebook = RuleBook([
        TMRule(1, '0', 2, '1', Direction.right),
        TMRule(1, '1', 1, '0', Direction.left),
        TMRule(1, '_', 2, '1', Direction.right),
        TMRule(2, '0', 2, '0', Direction.right),
        TMRule(2, '1', 2, '1', Direction.right),
        TMRule(2, '_', 3, '_', Direction.left)
    ])
    dtm = DTM(TMConfig(1, tape), [3], rulebook)
    assert dtm.is_accepted() == False
    dtm.step()
    assert dtm.is_accepted() == False
    dtm.run()
    assert dtm.is_accepted() == True


def test_TM_3():
    rulebook = RuleBook([
        TMRule(1, '0', 2, '1', Direction.right),
        TMRule(1, '1', 1, '0', Direction.left),
        TMRule(1, '_', 2, '1', Direction.right),
        TMRule(2, '0', 2, '0', Direction.right),
        TMRule(2, '1', 2, '1', Direction.right),
        TMRule(2, '_', 3, '_', Direction.left)
    ])
    tape = Tape.make('1211', 3)
    dtm = DTM(TMConfig(1, tape), [3], rulebook)
    dtm.run()
    assert dtm.is_stuck() == True

def test_TM_4():
    rulebook = RuleBook([
        TMRule(1, 'X', 1, 'X', Direction.right),
        TMRule(1, 'a', 2, 'X', Direction.right),
        TMRule(1, '_', 6, '_', Direction.left),

        TMRule(2, 'a', 2, 'a', Direction.right),
        TMRule(2, 'X', 2, 'X', Direction.right),
        TMRule(2, 'b', 3, 'X', Direction.right),

        TMRule(3, 'b', 3, 'b', Direction.right),
        TMRule(3, 'X', 3, 'X', Direction.right),
        TMRule(3, 'c', 4, 'X', Direction.right),

        TMRule(4, 'c', 4, 'c', Direction.right),
        TMRule(4, '_', 5, '_', Direction.left),

        TMRule(5, 'a', 5, 'a', Direction.left),
        TMRule(5, 'b', 5, 'b', Direction.left),
        TMRule(5, 'c', 5, 'c', Direction.left),
        TMRule(5, 'X', 5, 'X', Direction.left),

        TMRule(5, '_', 1, '_', Direction.right),
    ])
    tape = Tape.make('aaabbbccc')
    dtm = DTM(TMConfig(1, tape), [6], rulebook)
    dtm.run()
    assert dtm.is_stuck() == False
    assert dtm.is_accepted() == True


def test_TM_5():
    rulebook = RuleBook([
        TMRule(1, 'a', 2, 'a', Direction.right),
        TMRule(1, 'b', 3, 'b', Direction.right),
        TMRule(1, 'c', 4, 'c', Direction.right),

        TMRule(2, 'a', 2, 'a', Direction.right),
        TMRule(2, 'b', 2, 'b', Direction.right),
        TMRule(2, 'c', 2, 'c', Direction.right),
        TMRule(2, '_', 5, 'a', Direction.right),

        TMRule(3, 'a', 3, 'a', Direction.right),
        TMRule(3, 'b', 3, 'b', Direction.right),
        TMRule(3, 'c', 3, 'c', Direction.right),
        TMRule(3, '_', 5, 'b', Direction.right),

        TMRule(4, 'a', 4, 'a', Direction.right),
        TMRule(4, 'b', 4, 'b', Direction.right),
        TMRule(4, 'c', 4, 'c', Direction.right),
        TMRule(4, '_', 5, 'c', Direction.right),
    ])
    tape = Tape.make('bcabacca')
    assert repr(tape) == '(b)cabacca'
    dtm = DTM(TMConfig(1, tape), [5], rulebook)
    assert repr(dtm.current_config.tape) == '(b)cabacca'
    dtm.run()
    assert dtm.is_accepted() == True
    assert repr(dtm.current_config.tape) == 'bcabaccab(_)'
