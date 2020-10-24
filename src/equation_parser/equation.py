from __future__ import absolute_import

#SymPy is a non-commercial alternative to Mathematica and Maple
# SymPy can map variable to a value or a matrix.
# SymPy's Symbolic Statistical Modelling uses scintific computing.
import sys
import numpy as np
import sympy as sp
import pandas as pd
from .tokens import *

__all__ = ['Equation']

class Equation:
    def __init__(self, eq_string : str, X : pd.DataFrame ):
        """
        """
        self.expr = eq_string
        #give input equation
        self.tokens = Tokens(eq_string)
        if self.tokens.validate():
            print("valid tokens!")
        self.X = X
        self.symbols = None
        self.columns_mappings = dict()
        self.result = None
    
    def set_symbols(self, columns_symbol_mappings):
        if columns_symbol_mappings == "":
            #"x_1**2 + x_2*x_3")
            #get number of columns from X dataframe and y dataframe
            num_of_columns = len(self.X.columns)+1 #dataframe features len(X.columns) +1
            #create equation variables as user prefers to enter like x_1 ** 2 + x_2 * x_3
            symbols = sp.symarray('x',num_of_columns+1)
            self.symbols = symbols[1:]
        else:
            self.symbols = []
            self.columns_mappings = dict()
            for col, symbol in zip(columns_symbol_mappings['column'], 
                        columns_symbol_mappings['variable']):
                self.symbols.append(sp.symbols(symbol))
                self.columns_mappings[symbol] = col

    def evaluate(self):
        self.expression = sp.sympify(self.expr)
        #create variables SymPy way and store it as a stuple for creating f_1(x) -> H_1(x)
        variable_tuple = [self.X[c].to_numpy() for i,c in enumerate(self.X.columns, start=1)]

        #define the R.H.S of equation as user inputs and as parsed
        #expr =  x_1**2 + x_2*x_3
        #use lambdify with symbols that are actually created as variables and expression and 
        #package to be used
        f = sp.lambdify(self.symbols, self.expr, 'numpy')
        #replace features in f(x_1,x_2,x_3) => map x_1, x_2, x_3 to x1,x2,x3
        #evaluate
        self.result = f(*variable_tuple)
        print(self.result)
        return self.result