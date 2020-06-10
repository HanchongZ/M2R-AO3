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
        self.operand = operand

    def __repr__(self):
        return '{a}({b})'.format(a = self.__class__.__name__, b = repr(self.operand))

    def __str__(self):
        return '{a}'.format(a = self.operand)
    
    def diff(self, doperand, var):
        if self == var:
            return Number(1)
        else:
            return Number(0)

class Operator(Expression):
    pass

class Symbol(Terminal):

    #check if input is a string
    def __init__(self, operand):
        if type(operand) == str:
            Terminal.__init__(self, operand)
        else:
            print('error')

    def evaluation(self,eva):
        return eva
    
class Number(Terminal):

    #check if input is a number
    def __init__(self, operand):
        if type(operand) == int or type(operand) == float:
            Terminal.__init__(self, operand)
        else:
            print('error')

    def evaluation(self,eva):
        return self

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

    def evaluation(self,eva):
        return self.__class__(self.operand[0].evaluation(eva),self.operand[1].evaluation(eva))

class Add(Binary):

    symbol = ' + '
    priority = 1

    def __init__(self, *operand):
        self.operand = operand
    
    def diff(self, doperand, var):
        return doperand[0] + doperand[1]

class Sub(Binary):

    symbol = ' - '
    priority = 1

    def __init__(self, *operand):
        self.operand = operand
    
    def diff(self, doperand, var):
        return doperand[0] - doperand[1]    


class Mul(Binary):

    symbol = '*'
    priority = 2

    def __init__(self, *operand):
        self.operand = operand
    
    def diff(self, doperand, var):
        return doperand[0] * self.operand[1] + doperand[1] * self.operand[0] 

class Div(Binary):

    symbol = '/'
    priority = 2

    def __init__(self, *operand):
        self.operand = operand
    
    def diff(self, doperand, var):
        return (doperand[0] * self.operand[1] - doperand[1] * self.operand[0]) / (self.operand[1] * self.operand[1])

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


class Unary(Operator):

    def __init__(self, operand):
        self.operand = operand

    def __repr__(self):
        return '{a}({b})'.format(a = self.__class__.__name__, b = repr(self.operand))

    def __str__(self):
        return self.symbol+'{}'.format(self.operand)

    def evaluation(self,eva):
        return self.__class__(self.operand.evaluation(eva))
    
class UAdd(Unary):

    symbol = '+'
    priority = 3

    def diff(self, doperand, var):
        return doperand[0]    

class USub(Unary):

    symbol = '-'
    priority = 3
    
    def diff(self, doperand, var):
        return - doperand[0]

class Function(Operator):

    priority = 6

    def __init__(self, operand):
        self.operand = operand

    def __repr__(self):
        return '{a}({b})'.format(a = self.__class__.__name__, b = repr(self.operand))
    
    def __str__(self):
        return self.symbol+'({})'.format(self.operand)

    def evaluation(self,eva):
        return self.__class__(self.operand.evaluation(eva))

class Log(Function):
    
    symbol = 'log'
    
    def diff(self, doperand, var):
        return doperand[0] * Number(1) / self.operand

class Sin(Function):

    symbol = 'sin'

    def diff(self, doperand, var):
        return Cos(self.operand) * doperand[0]

class Cos(Function):

    symbol = 'cos'

    def diff(self, doperand, var):
        return - Sin(self.operand) * doperand[0]
    
def derivative(e,var):
    
    def diff(doperand):
        return e.diff(doperand,var)
    
    post_visit(e,diff)    

def post_visit(e, visit_fn):

    #initialize
    stack = [e]
    visited = {}

    while stack:

        #initialize
        temp = stack.pop()
        to_visit = []
        doperand = []
        
        if isinstance(temp, Binary):
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

        elif isinstance(temp, Unary) or isinstance(temp, Function):
            #if already visited, append derivatives onto doperand
            if repr(temp.operand) in visited.keys():
                doperand.append(visited[repr(temp.operand)])
            #if not in visited, add to to_visit
            else:
                to_visit.append(temp.operand)
                    
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

