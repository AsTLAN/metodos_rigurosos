# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 21:22:09 2013

@author: AndresAstorgaEspriella
"""
import numpy as np

class Taylor(object):

    def __init__(self, coef, orden = None):
        self.coef = coef
        self.orden = orden
        
        if not isinstance(coef, list):
                self.coef = [coef]
                
        
        if orden is None:
            self.orden = len(self.coef) - 1
            
    def __repr__(self):
        return "Taylor {}".format(self.coef)
    
    def __str__(self):
    # Esta función sirve con 'print'
        return "{}".format(self.coef)

    # Aquí vienen las operaciones aritméticas
    def __add__(self, otro):
        """
        Suma de Polinomios
        """
        try:
            a = max(self.orden, otro.orden)
        
        except:
            a = self.orden
        
        def s(x):
            if a == self.orden:
                if x <= otro.orden:
                    return self.coef[x] + otro.coef[x]
                
                if x > otro.orden:
                    return self.coef[x]
                
            if a == otro.orden:
                if x <= self.orden:
                    return self.coef[x] + otro.coef[x]
                
                if x > self.orden:
                   return otro.coef[x]     

        try:
            return Taylor([s(i) for i in range(0, a+1)], a)
        
        except:
            return self + Taylor(otro)
        
    def __radd__(self, otro):
        return self + otro
    
    def extend(self, m):
        if m <= self.orden:
            def ext1(x):
                if x <= m:
                    return self.coef[x]
                
                else:
                   return 0
            
            return Taylor([ext1(i) for i in range(0, m+1)], m)
        
        if m > self.orden:
            def ext2(x):
                if x <= self.orden:
                    return self.coef[x]
                
                else:
                   return 0
            
            return Taylor([ext2(i) for i in range(0, m+1)], m)     

    def __mul__(self, otro):
        """
        Multiplicación Polinomios
        """
        if not isinstance(otro, Taylor):
            otro = Taylor(otro) 
            
        if self.orden >= otro.orden:
            b = otro.extend(self.orden)
        
            def sumando1_m(n,i):
                return self.coef[i] * b.coef[n - i]
        
            def m1(n):
                return np.sum([(sumando1_m(n, i)) for i in range(0, n+1)])
        

            return Taylor([m1(i) for i in range(0, (self.orden)+1)])

        if otro.orden >= self.orden:
            c = self.extend(otro.orden)
        
            def sumando2_m(n,i):
                return c.coef[i] * otro.coef[n - i]
        
            def m2(n):
                return np.sum([(sumando2_m(n, i)) for i in range(0, n+1)])
        
            try:
                return Taylor([m2(i) for i in range(0, (otro.orden)+1)])
            
            except:
                return self *Taylor(otro)

    def __rmul__(self, otro):
        return self * otro
        
    def reciprocal(self):
        def d(n):
            if n == 0:
                return 1. / self.coef[0]
            
            if n ==1:
                return 1. / self.coef[0] *  (- d(0) * self.coef[1])
            
            else:
                return (1. / self.coef[0]) * (- np.sum([d(i) * self.coef[n - i] for i in range(0,n) ]))
                
        return Taylor([d(i) for i in range(0, self.orden + 1)], self.orden)
    
    def __div__(self, otro):
        if not isinstance (otro, Taylor):
            otro = Taylor(otro)
        
        a = otro.reciprocal()
        return self * a
        
    def __pow__(self, alpha):
        def a(n):
            if n == 0:
                return (self.coef[0])**(alpha)
            
            if n ==1:
                return 1./ a(0) * (alpha) * self.coef[1] * a(0)
            
            else:
                return ( 1. / a(0) ) * ( np.sum([ (((alpha + 1.) * i) / n - 1) * self.coef[i] * a(n-i) for i in range(1, n+1) ]) )
                
        return Taylor([a(i) for i in range(0, self.orden + 1)], self.orden)
    
    def exp(self):
        def e(n):
            if n == 0:
                return np.exp(self.coef[0])
            
            if n ==1:
                return e(0) * self.coef[1]
            
            else:
                return ( 1. / n ) * np.sum([i * e(n - i) * self.coef[i] for i in range(1, n+1) ])
                
        return Taylor([e(i) for i in range(0, self.orden + 1)], self.orden)
    
    def log(self):
        def l(n):
            if n == 0:
                return np.log(self.coef[0])
            if n == 1:
                return (1. / self.coef[0]) * (self.coef[1])
            
            else:
                return (1. / self.coef[0]) * ( self.coef[n] - (1. / n) * np.sum([i * l(i) * self.coef[n - i] for i in range(1, n) ]))
                
        return Taylor([l(i) for i in range(0, self.orden + 1)], self.orden)
        
    def sin(self):
        def si(n):
            if n == 0:
                return [np.sin(self.coef[0]), np.cos(self.cos[0])]
            
            if n == 1:
                return [self.coef[1] * si(0)[1], -self.coef[1] * si(0)[0]]
            
            else:
                return [(1. / n) * ( np.sum([i * self.coef[i] * si(n-i)[1] for i in range(1, n+1)]) ), -(1. / n) * ( np.sum([i * self.coef[i] * si(n-i)[0] for i in range(1, n+1)]) )]
        
        return Taylor([si(i)[0] for i in range(0, self.orden + 1)], self.orden)

    def cos(self):
        def co(n):
            if n == 0:
                return [np.sin(self.coef[0]), np.cos(self.cos[0])]
            
            if n == 1:
                return [self.coef[1] * co(0)[1], -self.coef[1] * co(0)[0]]
            
            else:
                return [(1. / n) * ( np.sum([i * self.coef[i] * co(n-i)[1] for i in range(1, n+1)]) ), -(1. / n) * ( np.sum([i * self.coef[i] * co(n-i)[0] for i in range(1, n+1)]) )]
        
        return Taylor([co(i)[1] for i in range(0, self.orden + 1)], self.orden)