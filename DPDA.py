from PDARule import *


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
