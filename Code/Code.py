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

    def diff(self, var):
        if self == var:
            return Number('1')
        else:
            return Number('0')

class Terminal(Expression):

    priority = 5

    def __init__(self, operand):
        self.operand = operand
        self.level = 0 #initialize level

    def __repr__(self):
        return '{a}({b})'.format(a = self.__class__.__name__, b = repr(self.operand))

    def __str__(self):
        return '{a}'.format(a = self.operand)


class Operator(Expression):
    pass

class Symbol(Terminal):
    pass

class Number(Terminal):
    pass

class Binary(Operator):
    def __str__(self):
        temp = []
        for a in self.operand:
            #if the operand inside has less priority add brackets
            if self.priority >= a.priority:
                a = '({})'.format(a)
            else:
                a = '{}'.format(a)
            temp.append(a)
        return self.symbol.join(x for x in temp)

class Add(Binary):

    symbol = '+'
    priority = 1

    def __init__(self, *operand):
        self.operand = operand
        self.level = max(a.level for a in operand) + 1

    def diff(self, var):
	#if operand is not a number, find its derivative in visited
        if not isinstance(self.operand[0], Number):
            a = visited['{h}'.format(h = repr(self.operand[0]))]
        else:
            a = self.operand[0]
        if not isinstance(self.operand[1], Number):
            b = visited['{k}'.format(k = repr(self.operand[1]))]
        else:
            b = self.operand[1]
	#add to visited if new term occurs
        if repr(a + b) not in visited:
            visited[repr(self.operand[0] + self.operand[1])] = a + b
        return a + b

class Sub(Binary):

    symbol = '-'
    priority = 1

    def __init__(self, *operand):
        self.operand = operand

class Mul(Binary):

    symbol = '*'
    priority = 2

    def __init__(self, *operand):
        self.operand = operand

class Div(Binary):

    symbol = '/'
    priority = 2

    def __init__(self, *operand):
        self.operand = operand

class Pow(Binary):

    symbol = '**'
    priority = 3

    def __init__(self, *operand):
        self.operand = operand

class Unary(Operator):

    def __repr__(self):
        return '{a}({b})'.format(a = self.__class__.__name__, b = repr(self.operand))

    def __str__(self):
        return self.symbol + '{}'.format(self.operand)

class UAdd(Unary):

    symbol = '+'
    priority = 0

    def __init__(self, operand):
        self.operand = operand

class USub(Unary):

    symbol = '-'
    priority = 0

    def __init__(self, operand):
        self.operand = operand



def derivative(e, var):
    #initialization
    global visited
    visited={}
    stack = [e]

    while stack != []:
        temp = stack.pop()
        if temp not in visited:
	    #if it is an operator the value is key itself
            if type(temp) != Symbol and type(temp) != Number:
                visited[repr(temp)] = temp
                for a in range(len(temp.operand)):
                    stack.append(temp.operand[a])
	    #if key is terminal, the value is its derivative
            else:
                visited[repr(temp)] = Terminal.diff(temp, var)
    #use a loop to update the derivatives
    for a in range(e.level):
	#use slice to avoid error for changing size in iteration
        temp = {k:visited[k] for k in dict.keys(visited)}
        keys = dict.keys(temp)
        for t in keys:
            if not isinstance(visited[t], Number):
                visited[t] = visited[t].diff(var)

    print(visited[repr(e)])
    return visited[repr(e)]
