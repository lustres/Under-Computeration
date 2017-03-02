def test_DPDA():
    import DPDA
    rulebook = DPDA.DPDARuleBook([
        DPDA.PDARule(1, '(', 2, '$', ['b', '$']),
        DPDA.PDARule(2, '(', 2, 'b', ['b', 'b']),
        DPDA.PDARule(2, ')', 2, 'b', []),
        DPDA.PDARule(2, None, 1, '$', ['$'])
    ])
    dpda_design = DPDA.DPDADesign(1, [1], rulebook)
    assert dpda_design.is_accepted('(((((((((())))))))))') == True
    assert dpda_design.is_accepted('()(())((()))(()(())))') == False
    assert dpda_design.is_accepted('(()(()(()()(()()))()') == False
    assert dpda_design.is_accepted('())') == False
