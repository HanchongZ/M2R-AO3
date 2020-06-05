# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""

from package import code_with_diff as Code
import sympy as sym
import pytest 


@pytest.fixture
def input_code():
    input = Code.Symbol('x') + Code.Symbol('y')
    return input


@pytest.fixture
def input_sym():
    input = sym.Symbol('x') + sym.Symbol('y')
    return input


@pytest.mark.print
def test_str(input_sym, input_code):
    assert input_sym.__str__() == input_code.__str__()
    
@pytest.mark.print
def test_repr(input_sym, input_code):
    assert sym.srepr(input_sym) == input_code.__repr__()


@pytest.mark.diff
def test_diff(input_sym2, input_code2):
    assert print(Code.derivative(input_code,Code.Symbol('x'))) == print(sym.diff(input_sym,sym.Symbol('x')))




