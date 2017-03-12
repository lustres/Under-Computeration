from enum import Enum

from base import Rule


class Tape(object):
    def __init__(self, left, middle, right, blank = '_'):
        super(Tape, self).__init__()
        self.left = left
        self.middle = middle
        self.right = right
        self.blank = blank

    def __repr__(self):
        return f'{"".join(list(map(str, self.left)))}({self.middle}){"".join(list(map(str, self.right)))}'

    def write(self, char):
        return Tape(self.left, char, self.right, self.blank)

    # [] X [X, X, X]
    #  <-|
    def move_head_left(self):
        if len(self.left) != 0:
            return Tape(self.left[:-1], self.left[-1], [self.middle] + self.right, self.blank)
        else:
            return Tape(self.left[:-1], self.blank, [self.middle] + self.right, self.blank)

    # [X, X, X] X []
    #           |->
    def move_head_right(self):
        if len(self.right) != 0:
            return Tape(self.left + [self.middle], self.right[0], self.right[1:], self.blank)
        else:
            return Tape(self.left + [self.middle], self.blank, self.right[1:], self.blank)

    @staticmethod
    def make(string, index=0, blank='_'):
        t = list(string)
        return Tape(t[0:index], t[index], t[index + 1:], blank)


class TMConfig(object):
    def __init__(self, state, tape):
        super(TMConfig, self).__init__()
        self.state = state
        self.tape = tape

    def __repr__(self):
        return f'<config state:{self.state} tape: {self.tape}>'

    def is_stuck(self):
        return self.state is None

    def stuck(self):
        return TMConfig(None, self.tape)


class Direction(Enum):
    left = 'L'
    right = 'R'


class TMRule(Rule):
    def __init__(self, state, char, next_state, write_char, direction):
        super(TMRule, self).__init__(state, char, next_state)
        self.write_char = write_char
        self.direction = direction

    def is_applied(self, config, char = None):
        return self.state == config.state and self.char == config.tape.middle

    def __repr__(self):
        return f'<rule {self.state}->{self.next_state} {self.char};{self.write_char}/{self.direction.value}>'

    def next_config(self, next_state, config):
        return TMConfig(next_state, self.next_tape(config))

    def next_tape(self, config):
        tape = config.tape.write(self.write_char)
        if self.direction == Direction.left:
            return tape.move_head_left()
        elif self.direction == Direction.right:
            return tape.move_head_right()
        else:
            raise TypeError()


class DTM(object):
    def __init__(self, current_config, accept_states, rulebook):
        super(DTM, self).__init__()
        self.current_config = current_config
        self.accept_states = accept_states
        self.rulebook = rulebook

    def is_accepted(self):
        return self.current_config.state in self.accept_states

    def is_stuck(self):
        return not self.is_accepted() and not self.rulebook.is_applied(self.current_config, None)

    def step(self):
        print(self.current_config)
        self.current_config = self.rulebook.next_config(self.current_config, None)
        return self

    def run(self):
        self.step()
        while not self.is_accepted() and not self.is_stuck():
            self.step()
        return self
