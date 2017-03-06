from PDARule import *


class NPDA(object):
    def __init__(self, _current_configs, accept_states, rulebook):
        super(NPDA, self).__init__()
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
        return len({config.state for config in self.current_configs} & self.accept_states) != 0


    def __read_char(self, char):
        self.current_configs = self.rulebook.next_configs(self.current_configs, char)
        return self

    def read_string(self, string):
        for c in string:
            self.__read_char(c)
        return self


class NPDADesign(object):
    def __init__(self, start_state, accept_states, rulebook, init_stack = ['$']):
        super(NPDADesign, self).__init__()
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook
        self.stack = Stack(init_stack)

    def __to_npda(self):
        config = PDAConfig(self.start_state, self.stack)
        return  NPDA({config}, self.accept_states, self.rulebook)

    def is_accepted(self, string):
        return self.__to_npda().read_string(string).is_accepted()
