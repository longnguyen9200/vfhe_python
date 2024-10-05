from imports import *
from number_untils import *
from polynomial_division import *
from typing import Union

def init_poly_modulus(poly_modulus: Union[int, np.array]) -> np.array:
    if isinstance(poly_modulus, int):
        return np.array([1] + [0] * (poly_modulus - 1) + [1], dtype=object)
    else:
        return poly_modulus

def add_zeros_to_higher_powers(poly: np.array,level:int):
    coef = np.append(poly,[0]* (level-len(poly)))
    return coef

class quotient_ring_poly:
    def __init__(
        self,
        coef_poly: np.array,
        coef_modulus:int,
        poly_modulus:Union[int, np.array],
        
    ):
        self._coef_poly= coef_poly
        self._coef_modulus = coef_modulus
        self._poly_modulus = init_poly_modulus(poly_modulus)
        self.level = len(poly_modulus)-1
        self._standardization()

    def _standardization(self):
        self._coef_poly = round_coef(self._coef_poly)
        self._coef_poly = mod_center(self._coef_poly, self.coef_modulus)
        _quotient,self._coef_poly = polydiv(self._coef_poly,self.poly_modulus)
        self._coef_poly = mod_center(self._coef_poly,self.coef_modulus)
        self._coef_poly = add_zeros_to_higher_powers(self._coef_poly,self.level)
        self._coef_poly = round_coef(self._coef_poly)

    def _check_qring(self, other):
        for i in range(len(self.poly_modulus)):
            if self.poly_modulus[i] != other.poly_modulus[i]:
                raise ValueError("It's not in the same quotient ring poly")
    
        if self.coef_modulus != other.coef_modulus:
            raise ValueError("It's not in the same quotient ring poly")
        
    def __neg__(self):
        return quotient_ring_poly(-self._coef_poly,self.coef_modulus, self.poly_modulus)
    
    def __add__(self, other):
        if isinstance(other,(int, float)):
            result = self.coef_poly+other
            return quotient_ring_poly(result,self.coef_modulus,self.poly_modulus)
        else:
            self._check_qring(other)
            result = polyadd(self._coef_poly,other.coef_poly)
            return quotient_ring_poly(result,self.coef_modulus,self.poly_modulus)
    
    def __sub__(self,other):
        return self+(-other)
    
    def __mul__(self, other):
        if isinstance(other,(int, float)):
            result = self.coef_poly*other
            return quotient_ring_poly(result,self.coef_modulus,self.poly_modulus)
        else:
            self._check_qring(other)
            result = polymul(self._coef_poly,other.coef_poly)
            return quotient_ring_poly(result,self.coef_modulus,self.poly_modulus)
    
    def __floordiv__(self, other):
        if isinstance(other,(int, float)):
            result = self.coef_poly//other
            return quotient_ring_poly(result,self.coef_modulus,self.poly_modulus)
        else:
            self._check_qring(other)
            quoctient, remainder = polydiv(self.coef_poly,other)
            return quotient_ring_poly(quoctient,self.coef_poly,self.coef_modulus)
        
    def __mod__(self, other):
        if isinstance(other,(int, float)):
            result = self.coef_poly%other
            return quotient_ring_poly(result,self.coef_modulus,self.poly_modulus)
        else:
            self._check_qring(other)
            quotient, remainder = polymul(self.coef_poly,other)
            return quotient_ring_poly(remainder,self.coef_poly,self.   coef_modulus)
        
    def __eq__(self,other):
        if all(x == y for x, y in zip(self._coef_poly, other.coef_poly)):
            if self.coef_modulus == other.coef_modulus:
                if all(a == b for a, b in zip(self.poly_modulus, other.poly_modulus)):
                    return True
        return False

    def copy(self) ->"quotient_ring_poly":
        return quotient_ring_poly(self.coef_poly, self.coef_modulus, self.poly_modulus)

    @property
    def poly_modulus(self):
        return self._poly_modulus.copy()

    @property
    def coef_modulus(self):
        return self._coef_modulus

    @coef_modulus.setter
    def coef_modulus(self, value):
        self._coef_modulus = value
        self._standardization()

    @property
    def coef_poly(self):
        return self._coef_poly

    @coef_poly.setter
    def coef_poly(self, value):
        self._coef_poly = value
        self._standardization()

    def __repr__(self):
        result = f"{self.coef_poly}, {self.coef_modulus}, {self.poly_modulus}"
        return result
    
    
