from sympy import Rational

class Nodo(object):
    def __init__(self, tiempo, punto, derivadas = None):
        # tiempo: Sympy Rational, int o float
        # punto: tupla de Sympy Rational, int o float
        # derivadas: lista de tuplas
        self.tiempo = Rational(tiempo)
        self.punto = punto_a_Rational(punto)
        if derivadas is None:
            self.derivadas = []
        else:
            self.derivadas = [ ( Rational(der[0]), Rational(der[1]) ) for der in derivadas ]

    @classmethod
    def from_dict(cls, datos):
        """
        Construye un nodo a partir de un diccionario datos, que contiene tiempo, punto y derivadas.
        """
        tiempo = Rational(datos["tiempo"])
        px, py = datos["punto"]
        punto = (Rational(px), Rational(py))
        derivadas = [(Rational(der[0]), Rational(der[1])) for der in datos["derivadas"]]

        return cls(tiempo, punto, derivadas)


    def to_dict(self):
        """
        Genera y devuelve un diccionario con los datos del nodo.
        """
        return {
            "tiempo": str(self.tiempo),
            "punto": (str(self.punto[0]), str(self.punto[1])),
            "derivadas": [(str(der[0]), str(der[1])) for der in self.derivadas]
        }
    
    def get_tiempo(self):
        return self.tiempo
    
    def get_punto(self):
        return self.punto
    
    def get_derivadas(self):
        return self.derivadas
    
    def set_tiempo(self, t):
        self.tiempo = Rational(t)
    
    def set_punto(self, p_nuevo):
        self.punto = punto_a_Rational(p_nuevo)

    def set_derivadas(self, der_list):
        self.derivadas = [punto_a_Rational(der) for der in der_list]
    
    def __str__(self):
        return f"Tiempo: {self.tiempo}\n" + f"Punto: {self.punto}\n" + f"Derivadas: {self.derivadas}"
    
    def __repr__(self):
        return str(self)
    
def punto_a_Rational(p):
    return (Rational(p[0]), Rational(p[1]))
