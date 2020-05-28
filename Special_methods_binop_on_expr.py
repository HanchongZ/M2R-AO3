# -*- coding: utf-8 -*-
"""
Created on Thu May 28 09:08:44 2020

@author: George
"""

class Expr:
    
    #add special method
    def __add__(self, other):
        return Add(self, other)
    
        #subtraction special method
    def __sub__(self, other):
        return Sub(self, other)
    
        #multiplication special method
    def __mul__(self, other):
        return Mul(self, other)
    
    #division special method
    def __div__(self, other):
        return Div(self,other)
    
    #power special method
    def __pow__(self,other):
        return Pow(self, other)

