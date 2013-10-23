# -*- coding: utf-8 -*-
import numpy as np

class Taylor(object):

    def __init__(self, coef, orden = None):
        self.coef = coef
        self.orden = orden
        
        if not isinstance(coef, list):
            self.coef = [coef]
            self.orden = 0
                
        if orden is None:
            self.orden = len(self.coef) - 1
            
        if len(self.coef) - 1 < self.orden:
            def ext(x):
                if x <= len(self.coef) -1:
                    return self.coef[x]
                else:
                    return 0
            self.coef = [ext(i) for i in range(self.orden + 1)]
        
        elif len(self.coef) -1 > self.orden:
            def restr(x):
                if x <= self.orden:
                    return self.coef[x]
                else:
                    return 0
            
            self.coef = [restr(i) for i in range(self.orden + 1)]
            
    def __repr__(self):
        return "Taylor {}".format(self.coef)
    
    def __str__(self):
        return "{}".format(self.coef)

    def __add__(self, otro):
        if not isinstance(otro, Taylor):
            otro = Taylor(otro)
        
        a = max(self.orden, otro.orden)
        
        def s(x):
            if self.orden >= otro.orden:
                if x <= otro.orden:
                    return self.coef[x] + otro.coef[x]
                
                if x > otro.orden:
                    return self.coef[x]
                
            elif  otro.orden > self.orden:
                if x <= self.orden:
                    return self.coef[x] + otro.coef[x]
                
                if x > self.orden:
                   return otro.coef[x]

        return Taylor([s(i) for i in range(a+1)], a)
    
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
        
        elif m >= self.orden:
            def ext2(x):
                if x <= self.orden:
                    return self.coef[x]
                
                else:
                   return 0
            
            return Taylor([ext2(i) for i in range(0, m+1)], m)

    def __mul__(self, otro):
        return self._mul1(otro)

    def _mul1(self, otro):
        if not isinstance(otro, Taylor):
            otro = Taylor(otro)
            
        if self.orden >= otro.orden:
            b = otro.extend(self.orden)
        
            def sumando1_m(n,i):
                return self.coef[i] * b.coef[n - i]
        
            def m1(n):
                return np.sum([sumando1_m(n, i) for i in range( n+1)])
        

            return Taylor([m1(i) for i in range(self.orden+1)], self.orden)

        elif otro.orden >= self.orden:
            c = self.extend(otro.orden)
        
            def sumando2_m(n,i):
                return c.coef[i] * otro.coef[n - i]
        
            def m2(n):
                return np.sum([(sumando2_m(n, i)) for i in range(n+1)])
        
            return Taylor([m2(i) for i in range(otro.orden+1)], otro.orden)

    def _mul2(self, otro, orden = None):
        if orden is None:
            orden = max(self.orden, otro.orden)
        self = self.extend(orden)
        otro = otro.extend(orden)
        def t(k):
            return np.sum([self.coef[i]*otro.coef[k-1] for i in range(k+1)])
        return Taylor([t(i) for i in range(orden+1)], orden)

    def __rmul__(self, otro):
        return self * otro

    def __neg__(self):
        coef = [-x for x in self.coef]
        return Taylor(coef, self.orden)
        
    def __sub__(self, otro):
        if not isinstance(otro, Taylor):
            otro = Taylor(otro)
        return self + (-a)
    
    def __rsub__(self, otro):
        if not isinstance(otro, Taylor):
            otro = Taylor(otro)
        return Taylor.__sub__(otro, self)
    
    def reciprocal(self):
        if not isinstance(self, Taylor):
            self = Taylor(self)
        
        def d(n):
            if n == 0:
                return 1. / self.coef[0]
            
            #elif n ==1:
            #    return 1. / self.coef[0] * (- d(0) * self.coef[1])
            
            else:
                return (1. / self.coef[0]) * (- np.sum([d(i) * self.coef[n - i] for i in range(n) ]))
                
        return Taylor([d(i) for i in range(self.orden + 1)], self.orden)
    
    #creo que esto puede ser más eficiente
    def _div2(self, otro, orden = None):
        if not isinstance(self, Taylor):
            self = Taylor(self)
        if orden is None:
            orden = max(self.orden, otro.orden)
        self = self.extend(orden)
        otro = otro.extend(orden)
        def d(k):
            if k == 0:
                return  self.coef[0]/float(otro.coef[0])
            else:
                return 1./otro.coef[0] * (self.coef[k]-np.sum([d(i)*otro.coef[k-i] for i in range(k)]))
        return Taylor([d(i) for i in range(orden+1)], orden)

    def _div1(self, otro):
        a = otro.reciprocal()
        return self * a

    def __div__(self, otro):
        return self._div1(otro)
    
    def __rdiv__(self, otro):
        if not isinstance (otro, Taylor):
            otro = Taylor(otro)
        b = self.reciprocal()       
        return otro * b
    
    def __pow__(self, otro):
        return self._pow1(otro)

    def __pow1(self, alpha):
        if not isinstance(self, Taylor):
            self = Taylor(self)        
        
        def a(n):
            if n == 0:
                return (self.coef[0])**(alpha)
            
            #elif n ==1:
            #    return 1./ sel.coef[0] * (alpha) * self.coef[1] * a(0)
            
            else:
                return ( 1. / self.coef[0] ) * ( np.sum([ (((alpha + 1.) * i) / n - 1) * self.coef[i] * a(n-i) for i in range(1, n+1) ]) )
                
        return Taylor([a(i) for i in range(self.orden + 1)], self.orden)
    
    def exp(self):
        def e(n):
            if n == 0:
                return np.exp(self.coef[0])
            
            #if n ==1:
            #    return e(0) * self.coef[1]
            
            else:
                return ( 1. / n ) * np.sum([i * e(n - i) * self.coef[i] for i in range(1, n+1) ])
                
        return Taylor([e(i) for i in range(0, self.orden + 1)], self.orden)
    
    def log(self):
        def l(n):
            if n == 0:
                return np.log(self.coef[0])
            #elif n == 1:
            #    return (1. / self.coef[0]) * (self.coef[1])
            
            else:
                return (1. / self.coef[0]) * ( self.coef[n] - (1. / n) * np.sum([i * l(i) * self.coef[n - i] for i in range(1, n) ]))
                
        return Taylor([l(i) for i in range(0, self.orden + 1)], self.orden)

    def _pow2(self, otro):
        return exp(otro*log(self))
        
    def sin(self):
        def si(n):
            if n == 0:
                return [np.sin(self.coef[0]), np.cos(self.cos[0])]
            
            #elif n == 1:
            #    return [self.coef[1] * si(0)[1], -self.coef[1] * si(0)[0]]
            
            else:
                return [(1. / n) * ( np.sum([i * self.coef[i] * si(n-i)[1] for i in range(1, n+1)]) ), -(1. / n) * ( np.sum([i * self.coef[i] * si(n-i)[0] for i in range(1, n+1)]) )]
        
        return Taylor([si(i)[0] for i in range(0, self.orden + 1)], self.orden)

    def cos(self):
        def co(n):
            if n == 0:
                return [np.sin(self.coef[0]), np.cos(self.cos[0])]
            
            #elif n == 1:
            #    return [self.coef[1] * co(0)[1], -self.coef[1] * co(0)[0]]
            
            else:
                return [(1. / n) * ( np.sum([i * self.coef[i] * co(n-i)[1] for i in range(1, n+1)]) ), -(1. / n) * ( np.sum([i * self.coef[i] * co(n-i)[0] for i in range(1, n+1)]) )]
        
        return Taylor([co(i)[1] for i in range(0, self.orden + 1)], self.orden)