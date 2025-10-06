import sympy as sp
from Codigo.Auxiliares.cambios_signo import cambios_signo

x, y, t = sp.symbols('x y t')
def nro_raices_sturm(f, intervalo1, intervalo2):
    """
    f es un polinomio de Sympy.
    Calcula el numero de raices que el polinomio f tiene en el intervalo (intervalo1, intervalo2)
    usando la secuencia de Sturm.
    intervalo1 < intervalo2 y no deben ser raíces de f
    """
    if f(intervalo1) == 0 or f(intervalo2) == 0:
        raise Exception("El polinomio no debe anularse en los extremos del intervalo")
    
    sturm_seq = sp.sturm(f)
    sturm_seq_int1 = [ f_i(intervalo1) for f_i in sturm_seq ]
    sturm_seq_int2 = [ f_i(intervalo2) for f_i in sturm_seq ]

    return  cambios_signo(sturm_seq_int1) - cambios_signo(sturm_seq_int2)

def nro_cortes(curva, recta, intervalo1, intervalo2):
    """
    Devuelve el numero de cortes de la curva (objeto de la clase Curva_Nodos) con la recta 
    entre los valores de parámetro intervalo1 e intervalo2.
    Suponemos que la curva no corta a la recta en t = intervalo1 ni en t = intervalo2.
    """
    curva_x = curva.xpoly
    curva_y = curva.ypoly

    if curva_x is None or curva_y is None:
        raise Exception("Curva no interpolada")

    f = sp.Poly(recta.subs({x: curva_x.as_expr(), y: curva_y.as_expr()}), t)
    return nro_raices_sturm(f, intervalo1, intervalo2)






