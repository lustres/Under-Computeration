class Variable:
    """
    Variable objects could be captured or passed in lambda expression
    """
    def __init__(self, name):
        """
        :type str
        :param name: a string used to refer this object
        """
        self.name = name

    def __repr__(self):
        return self.name


class Function:
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
        self.parameter = parameter
        self.body = body

    def __repr__(self):
        return f"lambda {self.parameter}: {self.body}"


class Call:
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
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left}({self.right})"
