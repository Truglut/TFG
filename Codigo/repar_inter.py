import os
import matplotlib.pyplot as plt
from ast import literal_eval
import sympy as sp
from clase_polinomio import *
from lectura_datos import *

def borrar(ax, grid = True):
    ax.clear()
    ax.grid(grid)

if __name__ == "__main__":
    t = sp.symbols('t')
    polinomios_guardar_dict = dict()
    sobreescribir = False
    ruta_archivo_polinomios = ""

    def guardar_polinomio(polinomio, nombre):
        guardar_en_dict(polinomio, polinomios_guardar_dict, nombre)
        print("Datos actuales del polinomio guardados en el diccionario 'polinomios_guardar_dict'."  \
              "El fichero .json se escribirá al cerrar el programa con exit(), quit() o Ctrl + D.")

    # Obtener datos para la interpolación del usuario
    tiempos_string = input("Tiempos en los que interpolar (separados por comas, fracciones entrecomilladas):\n")
    tiempos = literal_eval("[" + tiempos_string + "]")

    nodos = list()
    for t in tiempos:
        valores_string = input(f"Valor del polinomio en t = {t}: ")
        ders_string = input(f"Derivadas del polinomio en t = {t} (separadas por comas, fracciones entrecomilladas):\n")
        ders = literal_eval("[" + ders_string + "]")

        nodos.append(Nodo1d(t, valores_string, ders))
    

    f = PolinomioInterpolacion(nodos)
    print("Lista de nodos incorporada a un objeto PolinomioInterpolacion llamado 'f'")

    plt.ion()
    fig, ax = plt.subplots()
    ax.grid(True)

    # Si se han dado nodos de interpolación, graficamos el polinomio.
    if tiempos:
        f.interpolar()
        f.graficar(ax)

    plt.show(block=False)

    # Entrar en un REPL interactivo para poder añadir o modificar datos “sobre la marcha”
    try:
        from code import interact
        interact(local=globals())
    finally:
        if len(polinomios_guardar_dict) > 0:
            if ruta_archivo_polinomios == "":
                base = "polinomios"
            else:
                base = ruta_archivo_polinomios

            if base[-5:] != ".json":
                base += ".json"
            
            ruta_archivo_polinomios = base
            if not sobreescribir:
                i = 1
                while os.path.exists(ruta_archivo_polinomios):
                    ruta_archivo_polinomios = f"{base[:-5]}_{i}.json"
                    i += 1
            
            guardar_dict_en_archivo(ruta_archivo_polinomios, polinomios_guardar_dict)
            print(f"Curvas guardadas en el fichero '{ruta_archivo_polinomios}'")
        
