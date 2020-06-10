from Code import sym_sys as s
import sympy as sym
import pytest 

x = s.Symbol('x')
y = s.Symbol('y')

@pytest.fixture
def input_code():
    input = x ** s.Number(2) + x*y
    return input


@pytest.fixture
def input_sym():
    input = sym.Symbol('x') ** 2 + sym.Symbol('x')*sym.Symbol('y')
    return input

@pytest.fixture
def input_numberx():
	input = 2
	return input

@pytest.fixture
def input_numbery():
	input = 3
	return input


@pytest.mark.print
def test_str(input_sym, input_code):
    assert input_sym.__str__() == input_code.__str__()
    

@pytest.mark.print
def test_repr(input_sym, input_code):
    assert sym.srepr(input_sym) == input_code.__repr__()


@pytest.mark.diff
def test_diff(input_sym, input_code):
    assert print(s.simplify(s.derivative(input_code, x))) == print(sym.diff(input_sym, sym.Symbol('x')))


@pytest.mark.eval
def test_eval(input_sym, input_code, input_numberx, input_numbery):
	e = s.derivative(input_code, x)
	eva = s.evalue([x,y],[s.Number(input_numberx),s.Number(input_numbery)])
	assert s.evaluate(e,eva) == (sym.diff(input_sym,sym.Symbol('x'))).subs({sym.Symbol('x'):input_numberx,sym.Symbol('y'):input_numbery})




