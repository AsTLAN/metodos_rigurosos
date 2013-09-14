# -*- coding: utf-8 -*- 
class Intervalo(object):
    """
    Se define la clase 'Intervalo', y los métodos para la aritmética básica de intervalos, 
    es decir, suma, resta, multiplicación y división. Se incluyen otras funciones
    que serán útiles.
    """
    def __init__(self,lo,hi=None):
        """ 
        Definimos las propiedades del objeto Intervalo a partir de sus bordes,
        lo y hi, donde lo <= hi. En el caso en que el intervalo sólo tenga
        un número, éste se interpreta como un intervalo 'delgado' o 'degenerado'.
        """
        if hi is None:
            hi = lo
        elif (hi < lo):
            lo, hi = hi, lo
        
        self.lo = lo
        self.hi = hi
        
    def __repr__(self):
        return "Intervalo [{},{}]".format(self.lo,self.hi)
    
    def __str__(self):
        # Esta función sirve con 'print'
        return "[{},{}]".format(self.lo,self.hi)

    def _repr_html_(self):
        return "[{}, {}]".format(self.lo, self.hi)
    
    def _repr_latex_(self):
        return "$[{}, {}]$".format(self.lo, self.hi)

    # Aquí vienen las operaciones aritméticas
    def __add__(self, otro):
        """
        Suma de intervalos
        """
        try:
            return Intervalo(self.lo + otro.lo, self.hi + otro.hi)
        except:
            return self + Intervalo(otro)

    def __radd__(self, otro):
        return self + otro
    
    def __lt__(self,otro):
        '''Relación < de intervalos.'''
        
        try:
            return self.hi < otro.lo
        except:
            return self < Intervalo(otro)
        
    def __gt__(self,otro):
        '''Relación > de intervalos.'''
        
        try:
            return self.lo > otro.hi
        except:
            return self > Intervalo(otro)
    
    def __le__(self,otro):
	'''Relación <= de intervalos'''
	
        try: 
            return (self.lo <= otro.lo) and self.hi <= otro.hi
	
        except: 
            return self <= Intervalo(otro)

    def __ge__(self,otro):
	'''Relación >= de intervalos'''
	
        try:
            return (self.lo >= otro.lo) and self.hi >= otro.hi
        
        except: 
            return self >= Intervalo(otro)