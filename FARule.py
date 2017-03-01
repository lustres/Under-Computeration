class FARule(object):
    def __init__(self, state, char, next):
        super(FARule, self).__init__()
        self.state = state
        self.char = char
        self.next = next

    def is_applied(self, state, char):
        return self.state == state and self.char == char

    def follow(self):
        return self.next

    def __repr__(self):
        return f'#< {self.state} --[{self.char}]--> {self.next}) >'
