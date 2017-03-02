from PDARule import *

def test_DPDA():
    import DPDA
    rulebook = DPDA.DPDARuleBook([
        PDARule(1, '(', 2, '$', ['b', '$']),
        PDARule(2, '(', 2, 'b', ['b', 'b']),
        PDARule(2, ')', 2, 'b', []),
        PDARule(2, None, 1, '$', ['$'])
    ])
    dpda_design = DPDA.DPDADesign(1, [1], rulebook)
    assert dpda_design.is_accepted('(((((((((())))))))))') == True
    assert dpda_design.is_accepted('()(())((()))(()(())))') == False
    assert dpda_design.is_accepted('(()(()(()()(()()))()') == False
    assert dpda_design.is_accepted('())') == False


def test_DPDA_2():
    import DPDA
    rulebook = DPDA.DPDARuleBook([
        PDARule(1, 'a', 2, '$', ['a', '$']),
        PDARule(1, 'b', 2, '$', ['b', '$']),
        PDARule(2, 'a', 2, 'a', ['a', 'a']),
        PDARule(2, 'b', 2, 'b', ['b', 'b']),
        PDARule(2, 'a', 2, 'b', []),
        PDARule(2, 'b', 2, 'a', []),
        PDARule(2, None, 1, '$', ['$'])
    ])
    dpda_design = DPDA.DPDADesign(1, [1], rulebook)
    assert dpda_design.is_accepted('ababab') == True
    assert dpda_design.is_accepted('bbbaaaab') == True
    assert dpda_design.is_accepted('baa') == False


def test_NPDA():
    pass
