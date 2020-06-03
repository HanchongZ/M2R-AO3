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

    def __str__(self):
        pass

class Terminal(Expression):
    
    priority=5

    def __str__(self):
        return '{a}'.format(a=self.operand)


class Operator(Expression):    
    pass

class Symbol(Terminal):


    def __init__(self, operand):
        self.operand = operand

    def __repr__(self):
        return '{a}({b})'.format(a = self.__class__.__name__, b = repr(self.operand))


class Binary(Operator):
    def __str__(self):
        temp=[]
        for a in self.operand:
            #if the operand inside has less priority add brackets
            if self.priority >= a.priority:
                a='({})'.format(a)
            else:
                a='{}'.format(a)
            temp.append(a)
        return self.symbol.join( x for x in temp)

class Add(Binary):

    symbol='+'
    priority=1

    def __init__(self, *operand):
        self.operand = operand


class Sub(Binary):

    symbol='-'
    priority=1

    def __init__(self, *operand):
        self.operand = operand

class Mul(Binary):

    symbol='*'
    priority=2

    def __init__(self, *operand):
        self.operand = operand

class Div(Binary):

    symbol='/'
    priority=2

    def __init__(self, *operand):
        self.operand = operand

class Pow(Binary):

    symbol='**'
    priority=3

    def __init__(self, *operand):
        self.operand = operand

class Unary(Operator):

    def __repr__(self):
        return '{a}({b})'.format(a = self.__class__.__name__, b = repr(self.operand))

    def __str__(self):
        return self.symbol+'{}'.format(self.operand)

class UAdd(Unary):

    symbol='+'
    priority=4

    def __init__(self, operand):
        self.operand = operand

class USub(Unary):

    symbol='-'
    priority=4

    def __init__(self, operand):
        self.operand = operand


