from FARule import *


class DFARuleBook(object):
    def __init__(self, rules):
        super(DFARuleBook, self).__init__()
        self.rules = rules

    def next_config(self, config, char):
        rule = self.rule_for(config, char)
        if rule is not None:
            return rule.follow(config)
        else:
            return config.stuck()

    def rule_for(self, config, char):
        return next((i for i in self.rules if i.is_applied(config, char)), None)

    def __repr__(self):
        return self.rules.__repr__()


class DFA(object):
    def __init__(self, current_config, accept_states, rulebook):
        super(DFA, self).__init__()
        self.current_config = current_config
        self.accept_states = accept_states
        self.rulebook = rulebook

    def is_accepted(self):
        return self.current_config in self.accept_states

    def __read_char(self, char):
        if 'not_accepted' == self.current_config:
            return self
        s = self.rulebook.next_config(self.current_config, char)
        self.current_config = s if s is not None else 'not_accepted'
        return self

    def read_string(self, string):
        for c in string:
            self.__read_char(c)
        return self

    def __repr__(self):
        return f'current state: {self.current_config}'


class DFADesign(object):
    def __init__(self, start_state, accept_states, rulebook):
        super(DFADesign, self).__init__()
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def __to_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)

    def is_accepted(self, string):
        return self.__to_dfa().read_string(string).is_accepted()


def main():
    rulebook = DFARuleBook([
        FARule(1, 'a', 2), FARule(1, 'b', 1),
        FARule(2, 'a', 2), FARule(2, 'b', 3),
        FARule(3, 'a', 3), FARule(3, 'b', 3)
    ])
    dfa_design = DFADesign(1, [3], rulebook)
    print(dfa_design.is_accepted('a'))
    print(dfa_design.is_accepted('baa'))
    print(dfa_design.is_accepted('baba'))


if __name__ == '__main__':
    main()
