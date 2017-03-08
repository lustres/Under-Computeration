from step_semantic_base import *


class Machine(object):
    def __init__(self, statement, environment):
        super(Machine, self).__init__()
        self.statement = statement
        self.environment = environment

    def tick(self):
        reduced_ans = self.statement.reduce(self.environment)
        self.statement, self.environment = reduced_ans

    def run(self):
        while self.statement.is_reducible():
            print(f'{self.statement} <= {self.environment}')
            self.tick()
        print(f'{self.statement} <= {self.environment}')


Value.is_reducible = lambda self: False


Variable.reduce = lambda self, environment: environment[self.name]
Variable.is_reducible = lambda self: True


BinaryOper.reduce = abstractmethod(lambda self, environment: None)
BinaryOper.is_reducible = lambda self: True

# cause the lambda of python must be 'expression'

Add.reduce = lambda self, environment:\
    Add(self.left.reduce(environment), self.right)\
    if self.left.is_reducible()\
    else (Add(self.left, self.right.reduce(environment))
          if self.right.is_reducible()
          else Number(self.left.value + self.right.value))


Multiply.reduce = lambda self, environment:\
    Add(self.left.reduce(environment), self.right)\
    if self.left.is_reducible()\
    else (Add(self.left, self.right.reduce(environment))
          if self.right.is_reducible()
          else Number(self.left.value * self.right.value))


LessThan.reduce = lambda self, environment:\
    LessThan(self.left.reduce(environment), self.right)\
    if self.left.is_reducible()\
    else (LessThan(self.left, self.right.reduce(environment))
          if self.right.is_reducible()
          else Boolean(self.left.value < self.right.value))


Statement.is_reducible = lambda self: True


DoNothing.reduce = lambda self, environment:\
    NotImplementedError('Cannot be reduced')
DoNothing.is_reducible = lambda self: False


def sequence_reduce(self, environment):
    if self.first == DoNothing():
        return (self.second, environment)
    else:
        reduced_first, new_environment = self.first.reduce(environment)
        return (Sequence(reduced_first, self.second), new_environment)


Sequence.reduce = sequence_reduce


def assign_reduce(self, environment):
    if self.expression.is_reducible():
        new_stmt = Assign(self.name, self.expression.reduce(environment))
        return (new_stmt, environment)
    else:
        new_environment = dict(environment, **{self.name: self.expression})
        return (DoNothing(), new_environment)


Assign.reduce = assign_reduce


def if_reduce(self, environment):
    if self.condition.is_reducible():
        new_stmt = If(self.condition.reduce(environment),
                      self.consequence,
                      self.alternative)
        return (new_stmt, environment)
    else:
        if self.condition == Boolean(True):
            return (self.consequence, environment)
        elif self.condition == Boolean(False):
            return (self.alternative, environment)
        else:
            raise TypeError()


If.reduce = if_reduce


def while_reduce(self, environment):
    reduced = If(self.condition, Sequence(self.body, self), DoNothing())
    return (reduced, environment)


While.reduce = while_reduce


def main():
    Machine(
        While(
            LessThan(Variable('x'), Number(5)),
            Assign('x', Multiply(Variable('x'), Number(3)))),
        {'x': Number(1)}
    ).run()


if __name__ == '__main__':
    main()
