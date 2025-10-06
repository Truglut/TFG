import json
import sympy as sp
from Codigo.Curvas.clase_curva import *

def leer_poligonos_desde_json(ruta_fichero):
    """
    Lee el JSON y devuelve una lista de polígonos,
    donde cada polígono es una lista de tuplas (x, y).
    """
    with open(ruta_fichero, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    # Se asume que 'poligonos' existe y es lista de listas de pares [x,y]
    lista_poligonos = []
    for poly in datos.get("poligonos", []):
        # convertimos cada vértice [x, y] en tupla (x, y)
        tuplas_coordenadas = (tuple(sp.Rational(v[0]) for v in poly), tuple(sp.Rational(v[1]) for v in poly))
        lista_poligonos.append(tuplas_coordenadas)

    return lista_poligonos

def leer_curvas_desde_json(ruta_fichero):
    """
    Lee el JSON y devuelve un diccionario cuyos valores son objetos de la clase CurvaInterpolacion
    """

    with open(ruta_fichero, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    # Suponemos que hay una entrada 'curvas'
    curvas_dict = datos["curvas"]
    curvas_obj = dict()

    for nombre in curvas_dict:
        curvas_obj[nombre] = CurvaInterpolacion.from_dict(curvas_dict[nombre])

    return curvas_obj

def lista_curvas_desde_json(ruta_fichero):
    """
    Lee el json y devuelve una lista con las curvas guardadas en una lista en el fichero.
    """

    with open(ruta_fichero, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    return [CurvaInterpolacion.from_dict(c) for c in datos["curvas"]]

def leer_datos_desde_json(ruta_fichero):
    """
    Lee el fichero json y devuelve:
    - Una lista de los poligonos (representados por dos tuplas)
    - Una lista de curvas (como objetos CurvaInterpolacion)
    - Una lista de tiempos (sp.Rational)
    """

    with open(ruta_fichero, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    # Se asume que 'poligonos' existe y es lista de listas de pares [x,y]
    lista_poligonos = []
    for poly in datos.get("poligonos", []):
        # convertimos cada vértice [x, y] en tupla (x, y)
        tuplas_coordenadas = (tuple(sp.Rational(v[0]) for v in poly), tuple(sp.Rational(v[1]) for v in poly))
        lista_poligonos.append(tuplas_coordenadas)
    
    curvas = [CurvaInterpolacion.from_dict(c) for c in datos["curvas"]]
    tiempos = [sp.Rational(t) for t in datos["tiempos"]]
    tiempos_triangulos = [sp.Rational(ti) for ti in datos.get("tiempos_triangulos", [])]
    tiempos_triangulos_mal = [sp.Rational(ti) for ti in datos.get("tiempos_triangulos_mal", [])]
    intervalos_triangulos_mal = [(sp.Rational(intervalo[0]), sp.Rational(intervalo[1]))
                                 for intervalo in datos.get("intervalos_triangulos_mal", [])]
    

    repars = list()
    t = sp.symbols('t')
    for string_f in datos.get("reparametrizaciones", []):
        repars.append(sp.Poly(string_f, t))

    return lista_poligonos, curvas, tiempos, tiempos_triangulos, tiempos_triangulos_mal, intervalos_triangulos_mal, repars

def guardar_en_dict(objeto, diccionario, nombre=None):
    """
    Añade los datos actuales del objeto al diccionario para poder guardarlos posteriormente en
    un fichero json.
    El objeto debe tener un método .to_dict()
    """
    if nombre is None:
        nombre = str(type(objeto)) + str(len(diccionario))

    if nombre in diccionario.keys():
        print(f"Ya hay una curva guardada con el nombre '{nombre}'")
        s = ""
        while s != "y" or s != "n":
            s = input("¿Sobreescribir? (y/n)").lower()
        
        if s == "n":
            print("Vuelve a llamar a la función guardar_curva especificando otro nombre")
            return

    diccionario[nombre] = objeto.to_dict()
    return

def guardar_dict_en_archivo(ruta_fichero, diccionario):
    """
    Guarda los datos del diccionario en el fichero ruta_fichero
    *** Sobreescribe el fichero si ya existe ***
    """
    
    with open(ruta_fichero, 'w', encoding='utf-8') as f:
        json.dump(diccionario, f, ensure_ascii=False, indent=4)