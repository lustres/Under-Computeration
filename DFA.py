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
