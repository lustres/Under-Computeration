def test_step_semantic():
    import small_step_semantic
    import big_step_semantic
    small_step_semantic.main()
    big_step_semantic.main()


def test_DFA():
    import DFA
    rulebook = DFA.DFARuleBook([
        DFA.FARule(1, 'a', 2), DFA.FARule(1, 'b', 1),
        DFA.FARule(2, 'a', 2), DFA.FARule(2, 'b', 3),
        DFA.FARule(3, 'a', 3), DFA.FARule(3, 'b', 3)
    ])
    dfa_design = DFA.DFADesign(1, [3], rulebook)
    assert dfa_design.is_accepted('a') == False
    assert dfa_design.is_accepted('baa') == False
    assert dfa_design.is_accepted('baba') == True


def test_NFA():
    import NFA
    rulebook = NFA.NFARuleBook([
        NFA.FARule(1, None, 2), NFA.FARule(1, None, 4),
        NFA.FARule(2, 'a', 3), NFA.FARule(3, 'a', 2),
        NFA.FARule(4, 'a', 5), NFA.FARule(5, 'a', 6), NFA.FARule(6, 'a', 4)
    ])
    nfa_design = NFA.NFADesign(1, {2, 4}, rulebook)
    assert nfa_design.is_accepted('aa') == True
    assert nfa_design.is_accepted('aaa') == True
    assert nfa_design.is_accepted('aaaaa') == False
    assert nfa_design.is_accepted('aaaaaa') == True
