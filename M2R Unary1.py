class Expression:

    #initialize the operands
    def __init__(self, *operand):
        self.operand = operand
        
    #magic method for add
    def __add__(self, other):
        return Add(self, other)

    #magic method for division
    def __truediv__(self, other):
        return Div(self, other)

    #magic method for multi
    def __mul__(self, other):
        return Mul(self, other)

    #magic method for sub
    def __sub__(self, other):
        return Sub(self, other)

    #magic method for power
    def __pow__(self, other):
        return Pow(self, other)
    
    #magic method for unary plus
    def __pos__(self):
        return UAdd(self)
    
    #magic method for unary minus
    def __neg__(self):
        return USub(self)
    
    #magic method for repr
    #this is going to return what computer wants to read
    def __repr__(self):
        return '{a}({b})'.format(a = self.__class__.__name__, b = ','.join(repr(x) for x in self.operand))

    #magic method for str
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

    #initialize
    def __init__(self, *operand):
        self.operand = operand
        #define the mathematical expression
        self.math='{a} + {b}'.format(a = self.operand[0], b = self.operand[1])
        print('add method has been involked')        
     
class Sub(Binary):

    #initialize
    def __init__(self, *operand):
        self.operand = operand
        #define the mathematical expression
        self.math = '{a} - {b}'.format(a = self.operand[0], b = self.operand[1])
        print('sub method has been involked')

class Mul(Binary):

    #initialize
    def __init__(self, *operand):
        self.operand = operand
        #define the mathematical expression
        self.math = '{a} * {b}'.format(a = self.operand[0], b = self.operand[1])
        print('mul method has been involked')

class Div(Binary):

    #initialize
    def __init__(self, *operand):
        self.operand = operand
        #define the mathematical expression
        self.math = '{a} / {b}'.format(a = self.operand[0], b = self.operand[1])
        print('div method has been involked')

class Pow(Binary):

    #initialize
    def __init__(self, *operand):
        self.operand = operand
        #define the mathematical expression
        self.math = '{a} ** {b}'.format(a = self.operand[0], b = self.operand[1])
        print('pow method has been involked')

class Unary(Operator):
    
    #magic method for Unary operator
    def __repr__(self):
        return '{a}({b})'.format(a = self.__class__.__name__, b = repr(self.operand))

class UAdd(Unary):

    #initialize
    def __init__(self, operand):
        self.operand = operand
        #define the mathematical expression
        self.math = '+ {a}'.format(a = self.operand)
        print('unary add method has been involked') 

class USub(Unary):

    #initialize
    def __init__(self, operand):
        self.operand = operand
        #define the mathematical expression
        self.math = '- {a}'.format(a = self.operand)
        print('unary minus method has been involked')             
        
x = Symbol('x')
y = Symbol('y')
