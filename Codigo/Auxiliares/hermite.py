import sympy as sp
from Codigo.Curvas.nodos import *
t = sp.symbols('t')

def hermite_sympy_dicts(t_vals, valores_dict, ders_dict):
    """
    Halla el polinomio de interpolación de Hermite que toma los valores dados
    en el diccionario dado en valores_dict y con derivadas (hasta orden arbitrario) dadas en ders_dict.
    Todos los inputs (valores en t_vals, valores_dict y ders_dict) son Sympy Rationals.
    
    Parameters
    ----------
    t_vals : list
        [t0, t1, ..., tn], Sympy Rationals.
    valores_dict: dict
        {
        t0: f(t0)
        t1: f(t1)
        ...
        }
    ders_dict : diccionario de tuplas
        {  
          t0: (f'(t0), f''(t0), ..., f^(p0)(t0)),
          t1: (f'(t1), f''(t1), ..., f^(p1)(t1)),
          ...
        }
        The i-th tuple has length pi.
        
    Returns
    -------
    H : sympy Polynomial
        El polinomio de interpolación de Hermite en el símbolo 't'.
    """

    # 1. Construimos Z (lista de nodos) repitiendo cada t_i tantas veces como valores a interpolar
    Z = []
    for ti in t_vals:
        Z += [ti] * (len(ders_dict[ti]) + 1)
    N = len(Z)
    
    # 2. Primera columna de la tabla (columna 0): se repite f(t_i) para cada nodo en Z
    columna_cero = [valores_dict[ti] for ti in Z]

    for ti in t_vals:
        columna_cero += [valores_dict[ti]] * (len(ders_dict[ti]) + 1)
    
    # 3. Tabla de diferencias divididas: se construye columna a columna
    # tabla[k][i] contendrá la diferencia dividida f[Z_i,..., Z_{i+k}]
    tabla = [columna_cero]  # columna 0
    for k in range(1, N):
        col = []
        for i in range(N-k):
            if Z[i] == Z[i+k]:
                # nodo repetido k + 1 veces: usar la derivada de k-ésima dividida por k!
                deriv_value = ders_dict[Z[i]][k-1] # derivada k-ésima (k-1 porque se empieza en indice 0)
                col.append(deriv_value / sp.factorial(k))
            else:
                num = tabla[k-1][i+1] - tabla[k-1][i]
                den = Z[i+k] - Z[i]
                col.append(num/den)
        tabla.append(col)
    
    # 4. Construcción del polinomio usando los valores de la tabla
    H = 0
    termino = 1
    for k in range(N):
        H += tabla[k][0] * termino
        termino *= t - Z[k]
    H = sp.expand(H)
    return sp.Poly(H, t)

def curva_hermite_nodos(nodos):
    """
    Interpolación de curvas de Hermite en R2.
    Parameters
    ----------
    nodos: list
    Lista de nodos a interpolar, con tiempos, puntos y derivadas

    Returns
    -------
    curva_x : sympy Polynomial
        Polinomio interpolante de Hermite en x.
    curva_y : sympy Polynomial
        Polinomio interpolante de Hermite en y.
    """
    
    tiempos = [n.get_tiempo() for n in nodos]
    puntos_x = {n.get_tiempo(): n.get_punto()[0] for n in nodos}
    puntos_y = {n.get_tiempo(): n.get_punto()[1] for n in nodos}
    ders_x = {n.get_tiempo(): tuple(der[0] for der in n.get_derivadas()) for n in nodos}
    ders_y = {n.get_tiempo(): tuple(der[1] for der in n.get_derivadas()) for n in nodos}

    curva_x = hermite_sympy_dicts(tiempos, puntos_x, ders_x)
    curva_y = hermite_sympy_dicts(tiempos, puntos_y, ders_y)

    return curva_x, curva_y

def hermite_nodos(nodos):
    """
    Interpolación de polinomios de Hermite en R.
    Parameters
    ----------
    nodos: list
    Lista de nodos a interpolar, con tiempos, puntos y derivadas

    Returns
    -------
    sympy Polynomial
        Polinomio de Hermite interpolando los nodos dados.
    """
    # Los nodos deberían estar ordenados por tiempo, y sin repeticiones (no dos nodos con mismo tiempo)
    t_vals = [n.get_tiempo() for n in nodos]
    valores_dict = {n.get_tiempo(): n.get_valor() for n in nodos}
    ders_dict = {n.get_tiempo(): tuple(n.get_derivadas()) for n in nodos}

    return hermite_sympy_dicts(t_vals, valores_dict, ders_dict)