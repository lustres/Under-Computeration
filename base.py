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


class MultiRuleBook(object):
    def __init__(self, rules):
        super(MultiRuleBook, self).__init__()
        self.rules = rules

    def next_configs(self, configs, char):
        return {i for config in configs
                for i in self.follow_rules_for(config, char)}

    def follow_rules_for(self, config, char):
        return [rule.follow(config) for rule in self.rules_for(config, char)]

    def rules_for(self, config, char):
        return [i for i in self.rules if i.is_applied(config, char)]

    def follow_free_moves(self, configs):
        more_config = self.next_configs(configs, None)
        if more_config <= configs:
            return configs
        else:
            return self.follow_free_moves(more_config | configs)

    def __repr__(self):
        return self.rules.__repr__()
