class Expression:

    def __init__(self, *operand):
        self.operand = operand

    def __add__(self, other):
        return Add(self, other)

    def __truediv__(self, other):
        return Div(self, other)

    def __mul__(self, other):
        return Mul(self, other)

    def __sub__(self, other):
        return Sub(self, other)

    def __pow__(self, other):
        return Pow(self, other)

    def __pos__(self):
        return UAdd(self)

    def __neg__(self):
        return USub(self)

    def __repr__(self):
        return '{a}({b})'.format(a = self.__class__.__name__, b = ','.join(repr(x) for x in self.operand))

    #this is going to return what human wants to read
    def __str__(self):
        return self.math #mathematical expressions should be defined in each class


class Terminal(Expression):
    pass

class Operator(Expression):
    pass

class Symbol(Terminal):
    def __init__(self, operand):
        self.operand = operand
        self.math='{a}'.format(a = operand)
        print('symbol has been involked')

    #magic method for repr
    def __repr__(self):
        return '{a}({b})'.format(a = self.__class__.__name__, b = repr(self.operand))


class Binary(Operator):
    pass

class Add(Binary):

    def __init__(self, *operand):
        self.operand = operand
        #define the mathematical expression
        self.math='{a} + {b}'.format(a = self.operand[0], b = self.operand[1])

class Sub(Binary):

    def __init__(self, *operand):
        self.operand = operand
        #define the mathematical expression
        self.math = '{a} - {b}'.format(a = self.operand[0], b = self.operand[1])

class Mul(Binary):

    def __init__(self, *operand):
        self.operand = operand
        #define the mathematical expression
        self.math = '{a} * {b}'.format(a = self.operand[0], b = self.operand[1])

class Div(Binary):

    def __init__(self, *operand):
        self.operand = operand
        #define the mathematical expression
        self.math = '{a} / {b}'.format(a = self.operand[0], b = self.operand[1])

class Pow(Binary):

    def __init__(self, *operand):
        self.operand = operand
        #define the mathematical expression
        self.math = '{a} ** {b}'.format(a = self.operand[0], b = self.operand[1])

class Unary(Operator):

    def __repr__(self):
        return '{a}({b})'.format(a = self.__class__.__name__, b = repr(self.operand))

class UAdd(Unary):

    def __init__(self, operand):
        self.operand = operand
        #define the mathematical expression
        self.math = '+ {a}'.format(a = self.operand)

class USub(Unary):

    def __init__(self, operand):
        self.operand = operand
        #define the mathematical expression
        self.math = '- {a}'.format(a = self.operand)
