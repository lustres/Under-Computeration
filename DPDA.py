from PDARule import *


class DPDADesign(object):
    def __init__(self, start_state, accept_states, rulebook, init_stack = ['$']):
        super(DPDADesign, self).__init__()
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook
        self.stack = Stack(init_stack)

    def __to_dpda(self):
        config = PDAConfig(self.start_state, self.stack)
        return PDA(config, self.accept_states, self.rulebook)

    def is_accepted(self, string):
        return self.__to_dpda().read_string(string).is_accepted()
