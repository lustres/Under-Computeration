from functools import reduce


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

    def __repr__(self):
        return f'<config state:{self.state} stack: {self.stack}>'


class PDARule(object):
    def __init__(self, state, char, next_state, pop_char, push_chars):
        super(PDARule, self).__init__()
        self.state = state
        self.char = char
        self.next_state = next_state
        self.pop_char = pop_char
        self.push_chars = push_chars

    def __repr__(self):
        return f'<rule {self.state}->{self.next_state} {self.char};{self.pop_char}/{self.push_chars}>'

    def is_applied(self, config, char):
        return self.state == config.state and self.pop_char == config.stack.top() and self.char == char

    def follow(self, config):
        if not config.is_stuck():
            return PDAConfig(self.next_state, self.next_stack(config))
        else:
            return config.stuck()

    def next_stack(self, config):
        popped_stack = config.stack.pop()
        return reduce(lambda s, c: s.push(c), self.push_chars[::-1], popped_stack)


class DPDARuleBook(object):
    def __init__(self, rules):
        super(DPDARuleBook, self).__init__()
        self.rules = rules

    def next_config(self, config, char):
        rule = self.rule_for(config, char)
        if rule is not None:
            return rule.follow(config)
        else:
            return config.stuck()

    def rule_for(self, config, char):
        return next((i for i in self.rules if i.is_applied(config, char)), None)

    def is_applied(self, config, char):
        return self.rule_for(config, char) is not None

    def follow_free_moves(self, config):
        if self.is_applied(config, None):
            return self.follow_free_moves(self.next_config(config, None))
        else:
            return config

    def __repr__(self):
        return self.rules.__repr__()


class DPDA(object):
    def __init__(self, _current_config, accept_states, rulebook):
        super(DPDA, self).__init__()
        self.accept_states = accept_states
        self.rulebook = rulebook
        self._current_config = self.__config_with_free_move(_current_config)

    def __config_with_free_move(self, current):
        return self.rulebook.follow_free_moves(current)

    @property
    def current_config(self):
        return self._current_config

    @current_config.setter
    def current_config(self, value):
        self._current_config = self.__config_with_free_move(value)

    def is_accepted(self):
        return self.current_config.state in self.accept_states

    def __read_char(self, char):
        self.current_config = self.rulebook.next_config(self.current_config, char)
        return self

    def read_string(self, string):
        for c in string:
            self.__read_char(c)
        return self


class DPDADesign(object):
    def __init__(self, start_state, accept_states, rulebook, init_stack = ['$']):
        super(DPDADesign, self).__init__()
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook
        self.stack = Stack(init_stack)

    def __to_dpda(self):
        config = PDAConfig(self.start_state, self.stack)
        return DPDA(config, self.accept_states, self.rulebook)

    def is_accepted(self, string):
        return self.__to_dpda().read_string(string).is_accepted()


def main():
    rulebook = DPDARuleBook([
        PDARule(1, '(', 2, '$', ['b', '$']),
        PDARule(2, '(', 2, 'b', ['b', 'b']),
        PDARule(2, ')', 2, 'b', []),
        PDARule(2, None, 1, '$', ['$'])
    ])

    dpda_design = DPDADesign(1, [1], rulebook)
    print(dpda_design.is_accepted('(((((((((())))))))))'))
    print(dpda_design.is_accepted('()(())((()))(()(())))'))
    print(dpda_design.is_accepted('(()(()(()()(()()))()'))
    print(dpda_design.is_accepted('())'))


if __name__ == '__main__':
    main()
