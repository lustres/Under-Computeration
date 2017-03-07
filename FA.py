class FARule(object):
    def __init__(self, state, char, next):
        super(FARule, self).__init__()
        self.state = state
        self.char = char
        self.next = next

    def is_applied(self, state, char):
        return self.state == state and self.char == char

    def follow(self, config):
        return FAConfig(self.next)

    def __repr__(self):
        return f'#< {self.state} --[{self.char}]--> {self.next}) >'


class FAConfig(object):
    def __init__(self, state):
        super(FAConfig, self).__init__()
        self.state = state

    def stuck(self):
        return FAConfig(None)

    def is_stuck(self):
        return self.state is None

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash((self.state))

    def __repr__(self):
        return f'<config state:{self.state}>'


class FA(object):
    def __init__(self, _current_config, accept_states, rulebook):
        super(FA, self).__init__()
        self.accept_states = accept_states
        self.rulebook = rulebook
        self._current_config = self.__state_with_free_move(_current_config)

    def __state_with_free_move(self, current):
        return self.rulebook.follow_free_moves(current)

    @property
    def current_config(self):
        return self._current_config

    @current_config.setter
    def current_config(self, value):
        self._current_config = self.__state_with_free_move(value)

    def is_accepted(self):
        if isinstance(self.current_config, set):
            return len(({config.state for config in self.current_config} & self.accept_states)) != 0
        else:
            return self.current_config.state in self.accept_states

    def __read_char(self, char):
        self.current_config = self.rulebook.next_config(self.current_config, char)
        return self

    def read_string(self, string):
        for c in string:
            self.__read_char(c)
        return self

    def __repr__(self):
        return f'current state: {self.current_config}'


class FADesign(object):
    def __init__(self, start_config, accept_states, rulebook):
        super(FADesign, self).__init__()
        self.start_config = start_config
        self.accept_states = accept_states
        self.rulebook = rulebook

    def __to_fa(self):
        return FA(self.start_config, self.accept_states, self.rulebook)

    def is_accepted(self, string):
        return self.__to_fa().read_string(string).is_accepted()
