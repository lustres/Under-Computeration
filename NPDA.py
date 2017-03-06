from PDARule import *


class NPDADesign(object):
    def __init__(self, start_state, accept_states, rulebook, init_stack = ['$']):
        super(NPDADesign, self).__init__()
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook
        self.stack = Stack(init_stack)

    def __to_npda(self):
        config = PDAConfig(self.start_state, self.stack)
        return  PDA({config}, self.accept_states, self.rulebook)

    def is_accepted(self, string):
        return self.__to_npda().read_string(string).is_accepted()
