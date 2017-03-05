from TM import *


def test_TM_1():
    rule = TMRule(1, '0', 2, '1', Direction.right)
    print(rule)
    assert rule.is_applied(TMConfig(1, Tape([], '0', []))) == True
    assert rule.is_applied(TMConfig(1, Tape([], '1', []))) == False
    assert rule.is_applied(TMConfig(2, Tape([], '0', []))) == False


def test_TM_2():
    tape = Tape(['1', '0', '1'], '1', [])
    rulebook = DTMRuleBook([
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
    rulebook = DTMRuleBook([
        TMRule(1, '0', 2, '1', Direction.right),
        TMRule(1, '1', 1, '0', Direction.left),
        TMRule(1, '_', 2, '1', Direction.right),
        TMRule(2, '0', 2, '0', Direction.right),
        TMRule(2, '1', 2, '1', Direction.right),
        TMRule(2, '_', 3, '_', Direction.left)
    ])
    tape = Tape(['1', '2', '1'], '1', [])
    dtm = DTM(TMConfig(1, tape), [3], rulebook)
    dtm.run()
    assert dtm.is_stuck() == True

def test_TM_4():
    rulebook = DTMRuleBook([
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
    tape = Tape([], 'a', ['a', 'a', 'b', 'b', 'b', 'c', 'c', 'c'])
    dtm = DTM(TMConfig(1, tape), [6], rulebook)
    dtm.run()
    assert dtm.is_stuck() == False
    assert dtm.is_accepted() == True
