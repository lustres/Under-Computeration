from FARule import *


class NFARuleBook(object):
    def __init__(self, rules):
        super(NFARuleBook, self).__init__()
        self.rules = rules

    def next_states(self, states, char):
        '''return set() when matched rule not found'''
        return {i for state in states
                for i in self.follow_rules_for(state, char)}

    def follow_rules_for(self, state, char):
        return [rule.follow() for rule in self.rules_for(state, char)]

    def follow_free_moves(self, states):
        more_states = self.next_states(states, None)
        if more_states <= states:
            return states
        else:
            return self.follow_free_moves(more_states | states)

    def rules_for(self, state, char):
        return [i for i in self.rules if i.is_applied(state, char)]

    def __repr__(self):
        return self.rules.__repr__()


class NFA(object):
    def __init__(self, _current_state, accept_states, rulebook):
        super(NFA, self).__init__()
        self.accept_states = accept_states
        self.rulebook = rulebook
        self._current_state = self.__state_with_free_move(_current_state)

    def __state_with_free_move(self, current):
        return self.rulebook.follow_free_moves(current)

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, value):
        self._current_state = self.__state_with_free_move(value)

    def is_accepted(self):
        return len((self.current_state & self.accept_states)) != 0

    def __read_char(self, char):
        if 'not_accepted' in self.current_state:
            return self
        s = self.rulebook.next_states(self.current_state, char)
        self.current_state = s if s != set() else {'not_accepted'}
        return self

    def read_string(self, string):
        for c in string:
            self.__read_char(c)
        return self

    def __repr__(self):
        return f'current state: {self.current_state}'


class NFADesign(object):
    def __init__(self, start_state, accept_states, rulebook):
        super(NFADesign, self).__init__()
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def __to_nfa(self):
        return NFA({self.start_state}, self.accept_states, self.rulebook)

    def is_accepted(self, string):
        return self.__to_nfa().read_string(string).is_accepted()


def main():
    rulebook = NFARuleBook([
        FARule(1, None, 2), FARule(1, None, 4),
        FARule(2, 'a', 3), FARule(3, 'a', 2),
        FARule(4, 'a', 5), FARule(5, 'a', 6), FARule(6, 'a', 4)
    ])
    nfa_design = NFADesign(1, {2, 4}, rulebook)
    print(nfa_design.is_accepted('aa'))
    print(nfa_design.is_accepted('aaa'))
    print(nfa_design.is_accepted('aaaaa'))
    print(nfa_design.is_accepted('aaaaaa'))


if __name__ == '__main__':
    main()
