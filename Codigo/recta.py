import sympy as sp
x, y = sp.symbols('x y')

def ecuacion_recta(p1, p2):
    """
    Devuelve una expresión de sympy que corresponde a la ecuación de la recta que pasa
    por los puntos p1 y p2.
    Suponemos que p1 y p2 son puntos distintos
    """
    p1 = (sp.Rational(p1[0]), sp.Rational(p1[1]))
    p2 = (sp.Rational(p2[0]), sp.Rational(p2[1]))
    a = p2[1] - p1[1]
    b = p1[0] - p2[0]
    c = p2[0]*p1[1] - p2[1]*p1[0]

    a = sp.Rational(a)
    b = sp.Rational(b)
    c = sp.Rational(c)

    # Normalizamos la ecuación de la recta
    # Simplificar coeficientes
    d = sp.gcd(a,b,c)
    if isinstance(d, sp.Integer) and d > 1:
        a //= d
        b //= d
        c //= d

    # Asegurar que el coeficiente correspondiente a la variable 'y' es positivo
    if b < 0:
        a = -a
        b = -b
        c = -c
    # Si dicho coeficiente es nulo, ponemos el coeficiente de la 'x' en positivo
    elif b == 0 and a < 0: 
        a = -a
        c = -c
    
    return a*x + b*y + c

def crear_rectas(poligono):
    """
    poligono es una tupla con dos tuplas. La primera es la primera coordenada de cada uno de sus vértices,
    y la segunda tiene las segundas coordenadas. El primer punto y el último coinciden.
    Devuelve una lista de expresiones de Sympy, correspondientes a las ecuaciones de las
    rectas que delimitan el poligono.
    """
    
    n = len(poligono[0]) - 1 # número de vértices (el último está repetido)
    rectas_poligono = list()
    for i in range(n):
        p1 = (poligono[0][i], poligono[1][i])
        p2 = (poligono[0][i+1], poligono[1][i+1])

        rectas_poligono.append(ecuacion_recta(p1, p2))
    
    return rectas_poligono
    
