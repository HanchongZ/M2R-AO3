# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""

<<<<<<< HEAD
import symbolic_system as Code
=======
>>>>>>> 8224661b051686d00caa0b7aef90e5af9d91caea
import sympy as sym
import pytest 

x = Code.Symbol('x')
y = Code.Symbol('y')

@pytest.fixture
def input_code():
    input = x ** y 
    return input


@pytest.fixture
def input_sym():
    input = sym.Symbol('x') ** sym.Symbol('y') 
    return input


@pytest.mark.print
def test_str(input_sym, input_code):
    assert input_sym.__str__() == input_code.__str__()
    
@pytest.mark.print
def test_repr(input_sym, input_code):
    assert sym.srepr(input_sym) == input_code.__repr__()


@pytest.mark.diff
def test_diff(input_sym, input_code):
    assert print(Code.derivative(input_code, x)) == print(sym.diff(input_sym, sym.Symbol('x')))




