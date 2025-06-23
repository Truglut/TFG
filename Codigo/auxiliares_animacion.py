import numpy as np
from ast import literal_eval
import argparse

def crear_valores_t(t_intervals, frames_por_intervalo=100):
    """
    Crea una lista de valores de tiempo entre los intervalos especificados.

    Parameters:
    t_intervals (array-like): Lista de tiempos entre los que crear los valores.
    frames_por_intervalo (int): Número de frames en la animación en cada intervalo (t_intervals[i], t_intervals[i+1]).

    Returns:
    np.ndarray: Array de valores de tiempo.
    """
    if len(t_intervals) < 2:
        raise ValueError("t_intervals debe contener al menos dos valores de tiempo.")
    
    for i in range(len(t_intervals) - 1):
        if t_intervals[i] >= t_intervals[i + 1]:
            raise ValueError("Los valores de t_intervals deben estar en orden creciente.")
    
    t_vals = [np.linspace(t_intervals[i], t_intervals[i + 1], frames_por_intervalo, endpoint=False) for i in range(len(t_intervals) - 1)]
    t_vals.append([t_intervals[-1]])  # Añadir el último valor de t_intervals

    return np.concatenate(t_vals)

def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description="Dibuja polígonos leídos desde un fichero JSON"
    )
    parser.add_argument(
        "archivo_datos",
        help="Ruta al fichero JSON que contiene los datos para la animación: polígonos, curvas y reparametrizaciones"
    )
    parser.add_argument(
        "--frames_por_intervalo",
        help="Número de frames en cada intervalo entre los valores de t dados en el archivo de datos"
    )
    parser.add_argument(
        "--tiempo_animacion",
        help="Tiempo, en ms, que debe durar la animación (sin contar las paradas inicial y final)"
    )
    parser.add_argument(
        "--tiempo_fade_inicial",
        help="Tiempo en ms que tarda el triángulo en hacerse completamente visible"    
    )
    parser.add_argument(
        "--tiempo_parada_inicial",
        help="Tiempo en ms que la animación está parada antes de comenzar, pero después de que aparezca el triángulo"    
    )
    parser.add_argument(
        "--tiempo_parada_final",
        help="Tiempo en ms que la animación está parada después de terminar"
    )
    parser.add_argument(
        "--reparametrizaciones",
        help="Indica si se deben usar las reparametrizaciones dadas en el fichero. Debe ser un valor 'True', " \
        "'False', o un entero: 0 para False, 1 para True"
    )
    parser.add_argument(
        "--colores_poligonos",
        help="Lista (escrita con sintaxis de python y sin espacios) de los colores que se deben usar para dibujar" \
        "los poligonos"
    )
    parser.add_argument(
        "--alpha_figura",
        help="Valor de opacidad de los polígonos de fondo"
    )
    parser.add_argument(
        "--alpha_poligono_movil",
        help="Valor de opacidad del polígono que se va moviendo durante la animación"
    )
    parser.add_argument(
        "--alpha_poligonos_fijos",
        help="Valor de opacidad de los polígonos que se generan durante la animación, pero quedan fijos"
    )
    parser.add_argument(
        "--guardar_archivo",
        help="Ruta a un fichero en el que guardar la animación (como .gif)"
    )
    parser.add_argument(
        "--colores_curvas",
        help="Lista con los colores de las curvas"
    )
    parser.add_argument(
        "--alpha_curvas",
        help="Valor de opacidad de las curvas (tipo float)"
    )
    args = parser.parse_args()
    return args


def leer_argumentos(args):
    """
    Lee los argumentos escritos por el usuario en la terminal y devuelve los parámetros introducidos o,
    si no se han especificado, los valores por defecto.
    """
    
    parametros = dict()
    if args.frames_por_intervalo:
        frames_por_intervalo = int(args.frames_por_intervalo)
    else:
        frames_por_intervalo = 100
    parametros["frames_por_intervalo"] = frames_por_intervalo

    if args.tiempo_animacion:
        tiempo_animacion = int(args.tiempo_animacion)
    else:
        tiempo_animacion = 8000
    parametros["tiempo_animacion"] = tiempo_animacion
    
    if args.tiempo_fade_inicial:
        tiempo_fade_inicial = int(args.tiempo_fade_inicial)
    else:
        tiempo_fade_inicial = 400
    parametros["tiempo_fade_inicial"] = tiempo_fade_inicial
    
    if args.tiempo_parada_inicial:
        tiempo_parada_inicial = int(args.tiempo_parada_inicial)
    else:
        tiempo_parada_inicial = 500
    parametros["tiempo_parada_inicial"] = tiempo_parada_inicial
    
    if args.tiempo_parada_final:
        tiempo_parada_final = int(args.tiempo_parada_final)
    else:
        tiempo_parada_final = 500
    parametros["tiempo_parada_final"] = tiempo_parada_final

    if args.colores_poligonos:
        if args.colores_poligonos[0] == "[":
            colores_poligonos = literal_eval(args.colores_poligonos)
        else:
            colores_poligonos = [args.colores_poligonos]
    else:
        colores_poligonos = 'lightgray'
    parametros["colores_poligonos"] = colores_poligonos

    if args.alpha_figura:
        alpha_figura = float(args.alpha_figura)
    else:
        alpha_figura = 0.5
    parametros["alpha_figura"] = alpha_figura

    if args.colores_curvas:
        if args.colores_curvas[0] == "[":
            colores_curvas = literal_eval(args.colores_curvas)
        else:
            colores_curvas = [args.colores_curvas]
    else:
        colores_curvas = ["red", "green", "blue"]
    parametros["colores_curvas"] = colores_curvas

    if args.alpha_curvas:
        alpha_curvas = float(args.alpha_curvas)
    else:
        alpha_curvas = 0.5
    parametros["alpha_curvas"] = alpha_curvas

    if args.alpha_poligono_movil:
        alpha_poligono_movil = float(args.alpha_poligono_movil)
    else:
        alpha_poligono_movil = 0.5
    parametros["alpha_poligono_movil"] = alpha_poligono_movil
    
    if args.alpha_poligonos_fijos:
        alpha_poligonos_fijos = float(args.alpha_poligonos_fijos)
    else:
        alpha_poligonos_fijos = 0.5
    parametros["alpha_poligonos_fijos"] = alpha_poligonos_fijos

    if args.guardar_archivo:
        guardar = True
        ruta_archivo = args.guardar_archivo
    else:
        guardar = False
        ruta_archivo = None
    parametros["guardar"] = guardar
    parametros["ruta_archivo"] = ruta_archivo

    usar_repars = True
    if args.reparametrizaciones:
        s = args.reparametrizaciones.lower()
        if s == 'false' or s == 'f' or s == '0':
            usar_repars = False
        elif s == 'true' or s == 't' or s == '1':
            pass
        else:
            print("No se reconoce el parámetro introducido como 'reparametrizaciones'." \
            "Por defecto, se utilizan las reparametrizaciones si se han dado en el fichero.")
    parametros["usar_repars"] = usar_repars

    return parametros