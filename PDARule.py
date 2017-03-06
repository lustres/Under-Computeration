from functools import reduce
from base import Rule


class Stack(object):
    # Stack
    # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #  |                           |
    # top                        bottom
    def __init__(self, contents):
        self.contents = contents

    def push(self, char):
        return Stack([char] + self.contents)

    def pop(self):
        return Stack(self.contents[1:])

    def top(self):
        return self.contents[0]

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(tuple(self.contents))

    def __repr__(self):
        return f'<Stack ({self.top()}){"".join(list(map(str, self.contents[1:])))}>'


class PDAConfig(object):
    def __init__(self, state, stack):
        super(PDAConfig, self).__init__()
        self.state = state
        self.stack = stack

    def stuck(self):
        return PDAConfig(None, self.stack)

    def is_stuck(self):
        return self.state is None

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash((self.state, self.stack))

    def __repr__(self):
        return f'<config state:{self.state} stack: {self.stack}>'


class PDARule(Rule):
    def __init__(self, state, char, next_state, pop_char, push_chars):
        super(PDARule, self).__init__(state, char, next_state)
        self.pop_char = pop_char
        self.push_chars = push_chars

    def __repr__(self):
        return f'<rule {self.state}->{self.next_state} {self.char};{self.pop_char}/{self.push_chars}>'

    def is_applied(self, config, char):
        return self.state == config.state and self.pop_char == config.stack.top() and self.char == char

    def next_config(self, next_state, config):
        return PDAConfig(next_state, self.next_stack(config))

    def next_stack(self, config):
        popped_stack = config.stack.pop()
        return reduce(lambda s, c: s.push(c), self.push_chars[::-1], popped_stack)


class PDA(object):
    def __init__(self, _current_configs, accept_states, rulebook):
        super(PDA, self).__init__()
        self.accept_states = accept_states
        self.rulebook = rulebook
        self._current_configs = self.__config_with_free_move(_current_configs)


    def __config_with_free_move(self, current):
        return self.rulebook.follow_free_moves(current)

    @property
    def current_configs(self):
        return self._current_configs

    @current_configs.setter
    def current_configs(self, value):
        self._current_configs = self.__config_with_free_move(value)

    def is_accepted(self):
        if isinstance(self.current_configs, set):
            return len({config.state for config in self.current_configs} & self.accept_states) != 0
        else:
            return self.current_configs.state in self.accept_states


    def __read_char(self, char):
        self.current_configs = self.rulebook.next_config(self.current_configs, char)
        return self

    def read_string(self, string):
        for c in string:
            self.__read_char(c)
        return self
