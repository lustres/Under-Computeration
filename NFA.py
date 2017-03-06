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
        s = self.rulebook.next_configs(self.current_state, char)
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
