from step_semantic_base import *


Value.evaluate = lambda self, environment: self


Variable.evaluate = lambda self, environment: environment[self.name]


BinaryOper.evaluate = lambda self, environment, oper:\
    oper(self.left.evaluate(environment).value,
         self.right.evaluate(environment).value)


Add.evaluate = lambda self, environment:\
    Number(super(Add, self).evaluate(environment, lambda x, y: x + y))

Multiply.evaluate = lambda self, environment:\
    Number(super(Multiply, self).evaluate(environment, lambda x, y: x * y))

LessThan.evaluate = lambda self, environment:\
    Boolean(super(LessThan, self).evaluate(environment, lambda x, y: x < y))

DoNothing.evaluate = lambda self, environment:\
    environment

Sequence.evaluate = lambda self, environment:\
    self.second.evaluate(self.first.evaluate(environment))

Assign.evaluate = lambda self, environment:\
    dict(environment, **{self.name: self.expression.evaluate(environment)})


def if_evaluate(self, environment):
    judge = self.condition.evaluate(environment)
    if judge == Boolean(True):
        return self.consequence.evaluate(environment)
    elif judge == Boolean(False):
        return self.alternative.environment(environment)
    else:
        raise TypeError()


If.evaluate = if_evaluate


def while_evaluate(self, environment):
    judge = self.condition.evaluate(environment)
    if judge == Boolean(True):
        return self.evaluate(self.body.evaluate(environment))
    elif judge == Boolean(False):
        return environment
    else:
        raise TypeError()


While.evaluate = while_evaluate
