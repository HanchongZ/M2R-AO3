import math

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
        return '{a}({b})'.format(a = self.__class__.__name__, b = ', '.join(repr(x) for x in self.operand))
    
class Terminal(Expression):

    priority = 5

    def __init__(self, operand):
        self.operand = []
        self.operand.append(operand)

    def __str__(self):
        return '{a}'.format(a = self.operand[0])
        
    def diff(self, doperand, var):
        if self == var:
            return Number(1)
        else:
            return Number(0) 
        
    def simple(self,doperand):
        return self

class Symbol(Terminal):

    #check if input is a string
    def __init__(self, operand):
        if type(operand) == str:
            Terminal.__init__(self, operand)
        else:
            print('error')
    def evaluation(self,doperand,eva):
        num = eva[repr(self)]
        return num.operand[0]

    
class Number(Terminal):

    #check if input is a number
    def __init__(self, operand):
        if type(operand) == int or type(operand) == float:
           Terminal.__init__(self, operand)
        else:
            print('error')
            
    def evaluation(self,doperand,eva):
        return self.operand[0]   

class Operator(Expression):
    pass
    
class Binary(Operator):

    def __str__(self):
        temp = []
        for a in self.operand:
            #if the operand inside has less priority add brackets
            if self.priority > a.priority:
                a ='({})'.format(a)
            else:
                a ='{}'.format(a)
            temp.append(a)
        return self.symbol.join(x for x in temp)

class Add(Binary):

    symbol = ' + '
    priority = 1

    def __init__(self, *operand):
        self.operand = operand
    
    def diff(self, doperand, var):
        return doperand[0] + doperand[1]
    
    def evaluation(self, doperand,eva):
        return doperand[0] + doperand[1]
    
    def simple(self,doperand):
        if doperand[0].operand[0] == 0:
            return doperand[1]
        elif doperand[1].operand[0] == 0:
            return doperand[0]
        elif isinstance(doperand[0],Number) and isinstance(doperand[1],Number):
            return Number(doperand[0].operand[0] + doperand[1].operand[0])
        else:
            return self.__class__(doperand[0],doperand[1])
    

class Sub(Binary):

    symbol = ' - '
    priority = 1

    def __init__(self, *operand):
        self.operand = operand
    
    def diff(self, doperand, var):
        return doperand[0] - doperand[1]  
    
    def evaluation(self, doperand,eva):
        return doperand[0] - doperand[1]
    
    def simple(self,doperand):
        if doperand[0].operand[0] == 0:
            return -doperand[1]
        elif doperand[1].operand[0] == 0:
            return doperand[0]
        elif isinstance(doperand[0],Number) and isinstance(doperand[1],Number):
            return Number(doperand[0].operand[0] - doperand[1].operand[0])
        else:
            return self.__class__(doperand[0],doperand[1])

class Mul(Binary):

    symbol = '*'
    priority = 2

    def __init__(self, *operand):
        self.operand = operand
    
    def diff(self, doperand, var):
        return doperand[0] * self.operand[1] + doperand[1] * self.operand[0] 

    def evaluation(self, doperand,eva):
        return doperand[0] * doperand[1]
    
    def simple(self,doperand):
        if doperand[1].operand[0] == 1:
            return doperand[0]
        elif doperand[0].operand[0] == 1:
            return doperand[1]
        elif doperand[1].operand[0] == -1:
            return -doperand[1]
        elif doperand[0].operand[0] == -1:
            return -doperand[1]
        elif doperand[0].operand[0] == 0 or doperand[1].operand[0] == 0:
            return Number(0)
        elif isinstance(doperand[0],Number) and isinstance(doperand[1],Number):
            return Number(doperand[0].operand[0] * doperand[1].operand[0])
        else:
            return self.__class__(doperand[0],doperand[1])
        
class Div(Binary):

    symbol = '/'
    priority = 2

    def __init__(self, *operand):
        self.operand = operand
    
    def diff(self, doperand, var):
        return (doperand[0] * self.operand[1] - doperand[1] * self.operand[0]) / (self.operand[1] * self.operand[1])

    def evaluation(self, doperand,eva):
        return doperand[0] / doperand[1]
    
    def simple(self,doperand):
        if doperand[1].operand[0] == 1:
            return doperand[0]
        elif doperand[1].operand[0] == -1:
            return -doperand[0]
        elif doperand[1].operand[0] == 0:
            print('error')
        elif doperand[0].operand[0] == 0:
            return Number(0)
        elif isinstance(doperand[0],Number) and isinstance(doperand[1],Number):
            return Number(doperand[0].operand[0] / doperand[1].operand[0])
        else:
            return self.__class__(doperand[0],doperand[1])
    
class Pow(Binary):

    symbol = '**'
    priority = 4

    def __init__(self, *operand):
        self.operand = operand
    
    def diff(self, doperand, var):
        if isinstance(self.operand[1], Number):
            return self.operand[1] * self.operand[0] ** (self.operand[1] - Number(1)) * doperand[0]
        else:
            return self * (doperand[1] * Log(self.operand[0]) + self.operand[1] * doperand[0] / self.operand[0])
        
    def evaluation(self, doperand,eva):
        return doperand[0] ** doperand[1]
    
    def simple(self,doperand):
        if doperand[1].operand[0] == 1:
            return doperand[0]
        elif doperand[1].operand[0] == 0 or doperand[0].operand[0] == 1:
            return Number(1)
        elif doperand[0].operand[0] == 0:
            return Number(0)
        elif isinstance(doperand[0],Number) and isinstance(doperand[1],Number):
            return Number(doperand[0].operand[0] ** doperand[1].operand[0])
        else:
            return self.__class__(doperand[0],doperand[1])

class Unary(Operator):

    def __init__(self, operand):
        self.operand = []
        self.operand.append(operand)

    def __str__(self):
        return self.symbol+'{}'.format(self.operand[0])
    
    def simple(self,doperand):
        return self.__class__(doperand[0])
    
class UAdd(Unary):

    symbol = '+'
    priority = 3

    def diff(self, doperand, var):
        return doperand[0]    
    
    def evaluation(self, doperand,eva):
        return +doperand[0]

class USub(Unary):

    symbol = '-'
    priority = 3
    
    def diff(self, doperand, var):
        return - doperand[0]
    
    def evaluation(self, doperand,eva):
        return -doperand[0]

class Function(Operator):

    priority = 6

    def __init__(self, operand):
        self.operand = []
        self.operand.append(operand)

    
    def __str__(self):
        return self.symbol+'({})'.format(self.operand[0])
    
    def simple(self,doperand):
        return self.__class__(doperand[0])

class Log(Function):
    
    symbol = 'log'
    
    def diff(self, doperand, var):
        return doperand[0] * Number(1) / self.operand[0]
    
    def evaluation(self, doperand,eva):
        return math.log(doperand[0])


class Sin(Function):

    symbol = 'sin'

    def diff(self, doperand, var):
        return Cos(self.operand[0]) * doperand[0]
    
    def evaluation(self, doperand,eva):
        return math.sin(doperand[0])
    

class Cos(Function):

    symbol = 'cos'

    def diff(self, doperand, var):
        return - Sin(self.operand[0]) * doperand[0]
    
    def evaluation(self, doperand,eva):
        return math.cos(doperand[0])
    
def derivative(e,var):
    
    def diff(doperand):
        return temp.diff(doperand,var)
    
    return post_visit(e,diff)


def evalue(symbol,value):
    
    eva={}
        
    for a in range(len(symbol)):
        eva[repr(symbol[a])] = value[a]
    
    return eva
    
def evaluate(e,eva):
    
    def evaluation(doperand):
        return temp.evaluation(doperand,eva)
    
    return post_visit(e,evaluation)

def simplify(e):
    
    def simple(doperand):
        return temp.simple(doperand)
    
    return post_visit(e,simple)
        
def post_visit(e, visit_fn):
    
    global temp
    #initialize
    stack = [e]
    visited = {}

    while stack:

        #initialize
        temp = stack.pop()
        to_visit = []
        doperand = []
        
        if isinstance(temp, Operator):
            for o in temp.operand:
                #if already visited, append derivatives onto doperand
                if repr(o) in visited.keys():
                    doperand.append(visited[repr(o)])
                #if not in visited, add to to_visit
                else:
                    to_visit.append(o)
                    
            #add tovisit to the stack
            if to_visit:
                stack.append(temp)
                stack += to_visit
            #if all operands is in visited, apply chain rule
            else:
                visited[repr(temp)] = visit_fn(doperand)

        #if e is a terminal
        else:
            visited[repr(temp)] = visit_fn(doperand)
            
    return visited[repr(e)]