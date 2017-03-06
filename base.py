class Rule(object):
    def __init__(self, state, char, next_state):
        super(Rule, self).__init__()
        self.state = state
        self.char = char
        self.next_state = next_state

    def follow(self, config):
        if not config.is_stuck():
            return self.next_config(self.next_state, config)
        else:
            return config.stuck()

    def next_config(self, next_state, config):
        raise NotImplementedError()
