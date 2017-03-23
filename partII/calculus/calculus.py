class Term(object):
    def __init__(self):
        super(Term, self).__init__()


class Variable(Term):
    """
    Variable objects could be captured or passed in lambda expression.
    """
    def __init__(self, name):
        """
        :type str
        :param name: a string used to refer this object
        """
        super(Variable, self).__init__()
        self.name = name

    def replace(self, name, another):
        """
        replace a variable with another expression.
        :type str
        :param name: name of aim variable
        :param another: an expression used to replace
        :type Variable
        :return: expression passed in if name marched or self
        """
        if self.name == name:
            return another
        else:
            return self

    def bound_vars(self):
        """
        Variable never bound variable.
        """
        return {}

    def free_vars(self):
        """
        Variable always introduce free variable into context.
        """
        return {self.name}

    def reduce(self):
        return self

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Variable({repr(self.name)})"


class Function(Term):
    """
    Function objects represent a single parameter lambda expression.
    """
    def __init__(self, parameter, body):
        """
        :type str
        :param parameter: the name of variable which passed in

        :type Function | Call | Variable
        :param body: the rest of lambda
        """
        super(Function, self).__init__()
        self.parameter = parameter
        self.body = body

    def replace(self, name, another):
        """
        replace a free variable in the body of this function with another expression.
        if body doesn't have matched free variable, the method return self
        if you want replace a bound variable, use `alpha` instead
        :type str
        :param name: name of aim variable
        :param another: an expression used to replace
        :type Function
        :return: function after replace in if name marched or self
        """
        if name not in self.free_vars():
            # don't have aim free var
            return self
        elif self.bound_vars() & another.free_vars():
            # capture conflict
            # use alpha conversion to rename bound var aka. parameter
            return alpha(self, rename_policy(self.parameter)).replace(name, another)
        else:
            # have aim free var
            # no conflict
            return Function(self.parameter, self.body.replace(name, another))

    def bound_vars(self):
        """
        Function only bound variable once as its parameter.
        """
        return {self.parameter}

    def free_vars(self):
        """
        Function will bound its parameter on body.
        """
        return self.body.free_vars() - self.bound_vars()

    def reduce(self):
        return Function(self.parameter, self.body.reduce())

    def __str__(self):
        return f"lambda {self.parameter}: {self.body}"

    def __repr__(self):
        return f"Function({repr(self.parameter)}, {repr(self.body)})"

def alpha(func, rename, aim = None):
    """
    :type Function
    :param func:
    :type Variable
    :param rename:
    """
    if isinstance(func, Function):
        if aim is None:
            # first call
            # replace parameter and apply `alpha` to body
            return Function(rename, alpha(func.body, rename, func.parameter))
        else:
            # not first call
            if func.parameter is aim:
                # inner bounded
                return func
            else:
                # apply `alpha` to body
                return Function(func.parameter, alpha(func.body, rename, aim))
    elif isinstance(func, Call):
        return Call(alpha(func.left, rename, aim), alpha(func.right, rename, aim))
    elif isinstance(func, Variable):
        if func.name == aim:
            return rename
        else:
            return func


def beta(func, argument):
    """
    :type Function
    :param func:
    """
    return func.body.replace(func.parameter, argument)


def eta(func):
    """
    :type Function
    :param func:
    """
    if isinstance(func.body, Call) \
            and str(func.body.right) is func.parameter \
            and func.parameter not in func.body.left.free_vars():
        return func.body.left
    else:
        return func


def rename_policy(name):
    return Variable(name + "'")


class Call(Term):
    """
    Call objects define a call action on an entity.
    """
    def __init__(self, left, right):
        """
        :type Function | Call | Variable
        :param left: called entity
        :type Function | Call | Variable
        :param right: the parameter which will be passed in
        """
        super(Call, self).__init__()
        self.left = left
        self.right = right

    def replace(self, name, another):
        """
        replace a variable in this call with another expression.
        :type str
        :param name: name of aim variable
        :param another: an expression used to replace
        :type Call
        :return: Call after replace in if name marched or self
        """
        return Call(self.left.replace(name, another), self.right.replace(name, another))

    def reduce(self):
        """
        reduce a call expression
        This method will call `reduce` on two parts recursively.
        And then make call on it self.
        """
        # reduce argument first
        if is_reducible(self.right):
            return Call(self.left, self.right.reduce())
        elif is_reducible(self.left):
            return Call(self.left.reduce(), self.right)
        elif isinstance(self.left, Function):
            # reduce all part so make call
            return beta(self.left, self.right)
        else:
            # reduce all part and finish
            return self

    def bound_vars(self):
        """
        Call never bound variable cause all bounded value inside are not visible outside.
        """
        return {}

    def free_vars(self):
        """
        All free variable in sub pair of Call are still visible outside.
        """
        return self.left.free_vars() | self.right.free_vars()

    def __str__(self):
        if isinstance(self.left, Function):
            return f"({self.left})({self.right})"
        else:
            return f"{self.left}({self.right})"

    def __repr__(self):
        return f"Call({repr(self.left)}, {repr(self.right)})"


def is_reducible(term):
    """
    check a term whether reducible, raise a TypeError when term is not Variable, Function or Call
    :type Variable | Function | Call
    :param term: must be a instance of Variable, Function or Call
    :type bool
    :return: True if term is reducible or False
    """
    if isinstance(term, Variable) or isinstance(term, Function):
        return False
    elif isinstance(term, Call):
        return is_reducible(term.left) or is_reducible(term.right) or isinstance(term.left, Function)


def reduce(term):
    while is_reducible(term):
        term = term.reduce()

    while True:
        new_term = term.reduce()
        if str(new_term) == str(term):
            break
        term = new_term

    return term
