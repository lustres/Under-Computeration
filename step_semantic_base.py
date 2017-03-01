from abc import ABC, abstractmethod


class Value(object):
    def __init__(self, value):
        super(Value, self).__init__()
        self.value = value

    def __repr__(self):
        return f'<< {self} >>'

    def __str__(self):
        return self.value.__str__()


class Number(Value):
    def __init__(self, value):
        super(Number, self).__init__(value)

    def __eq__(self, other_bool):
        return self.__dict__ == other_bool.__dict__


class Boolean(Value):
    def __init__(self, value):
        super(Boolean, self).__init__(value)

    def __eq__(self, other_bool):
        return self.__dict__ == other_bool.__dict__


class Variable(object):
    def __init__(self, name):
        super(Variable, self).__init__()
        self.name = name

    def __repr__(self):
        return f'<< {self} >>'

    def __str__(self):
        return self.name.__str__()


class BinaryOper(ABC):
    def __init__(self, oper_name, left, right):
        super(BinaryOper, self).__init__()
        self.left = left
        self.right = right
        self.oper_name = oper_name

    def __repr__(self):
        return f'<< {self} >>'

    def __str__(self):
        return f'{self.left} {self.oper_name} {self.right}'


class Add(BinaryOper):
    def __init__(self, left, right):
        super(Add, self).__init__('+', left, right)


class Multiply(BinaryOper):
    def __init__(self, left, right):
        super(Multiply, self).__init__('*', left, right)


class LessThan(BinaryOper):
    def __init__(self, left, right):
        super(LessThan, self).__init__('<', left, right)


class Statement(ABC):
    def __init__(self):
        super(Statement, self).__init__()

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return f'<< {self} >>'


class DoNothing(Statement):
    def __init__(self):
        super(DoNothing, self).__init__()

    def __eq__(self, other_stmt):
        return isinstance(other_stmt, DoNothing)

    def __str__(self):
        return 'do-nothing'


class Sequence(Statement):
    def __init__(self, first, second):
        super(Sequence, self).__init__()
        self.first = first
        self.second = second

    def __str__(self):
        return f'{self.first}; {self.second}'


class Assign(Statement):
    def __init__(self, name, expression):
        super(Assign, self).__init__()
        self.name = name
        self.expression = expression

    def __str__(self):
        return f'{self.name} = {self.expression}'


class If(Statement):
    def __init__(self, condition, consequence, alternative):
        super(If, self).__init__()
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        # TODO:
        return f'if ({self.condition}) {"{"} {self.consequence} {"}"} else {"{"} self.alternative {"}"}'


class While(Statement):
    def __init__(self, condition, body):
        super(While, self).__init__()
        self.condition = condition
        self.body = body

    def __str__(self):
        # TODO:
        return f'while ({self.condition}) {"{"} {self.body} {"}"}'
