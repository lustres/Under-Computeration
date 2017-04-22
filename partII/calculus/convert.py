import ast, sys

import calculus


class Assign(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{str(self.left)} = {repr(self.right)}"


class LambdaBuilder(object):
    def __init__(self):
        super(LambdaBuilder, self).__init__()

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, None)
        return visitor(node) if visitor else None

    def visit_Module(self, node):
        stmts = list()
        for stmt in node.body:
            r = self.visit(stmt)
            if r:
                stmts.append(r)
        return stmts

    def visit_Assign(self, node):
        return Assign(self.visit(node.targets[0]), self.visit(node.value))

    def visit_Name(self, node):
        return calculus.Variable(node.id)

    def visit_Lambda(self, node):
        return calculus.Function(node.args.args[0].arg, self.visit(node.body))

    def visit_Call(self, node):
        return calculus.Call(self.visit(node.func), self.visit(node.args[0]))


def main():
    with open(sys.argv[1], 'r') as fin:
        code = fin.read()
        l = LambdaBuilder().visit(ast.parse(code))
        with open(sys.argv[2], 'w') as fout:
            for line in l:
                fout.write(repr(line))
                fout.write('\n')
            fout.write('\n')


if __name__ == '__main__':
    main()
