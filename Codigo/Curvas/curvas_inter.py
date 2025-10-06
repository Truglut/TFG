import os
import argparse
import matplotlib.pyplot as plt
from Codigo.Auxiliares.lectura_datos import *
from Codigo.Auxiliares.sturm import *
from Codigo.Auxiliares.cambios_signo import signo
from Codigo.Auxiliares.graficas import dibujar_poligonos

if __name__ == "__main__":
    print("Iniciando...")
    curvas_guardar_dict = dict()
    ruta_archivo_curvas = ""
    sobreescribir = False
    
    def guardar_curva(curva, nombre = None):
        guardar_en_dict(curva, curvas_guardar_dict, nombre)
        print("Datos actuales de la curva guardados en el diccionario 'curvas_guardar_dict'."  \
              "El fichero .json se escribirá al cerrar el programa con exit(), quit() o Ctrl + D.")

    # 1. Parsear argumento de entrada (ruta al JSON)
    parser = argparse.ArgumentParser(
        description="Dibuja polígonos leídos desde un fichero JSON"
    )
    parser.add_argument(
        "archivo_poligonos",
        help="Ruta al fichero JSON que contiene los polígonos"
    )
    # Argumento opcional para cargar curvas desde un archivo
    parser.add_argument(
        "--archivo_curvas",
        help="Ruta al fichero JSON que contiene datos sobre curvas ya calculadas"
    )
    args = parser.parse_args()

    # 2. Leer todos los polígonos desde el JSON (y curvas si se ha proporcionado un archivo)
    ruta_poligono = args.archivo_poligonos
    lista_poligonos = leer_poligonos_desde_json(ruta_poligono)
    print("Polígonos leídos")

    # Determinamos los límites de la figura
    xmin = float(min(vx for poly in lista_poligonos for vx in poly[0]))
    xmax = float(max(vx for poly in lista_poligonos for vx in poly[0]))
    ymin = float(min(vy for poly in lista_poligonos for vy in poly[1]))
    ymax = float(max(vy for poly in lista_poligonos for vy in poly[1]))
    
    if args.archivo_curvas:
        ruta_curvas = args.archivo_curvas
        curvas_dict = leer_curvas_desde_json(ruta_curvas)
        print("Curvas leídas, guardadas en el diccionario 'curvas_dict'")

    def borrar(ax):
        ax.clear()
        dibujar_poligonos(ax, lista_poligonos)

    # 3. Crear la figura de Matplotlib
    plt.ion()                           # modo interactivo ON
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')       # para que no deforme escalas
    ax.set_xlim(xmin - 1, xmax + 1)     # márgenes
    ax.set_ylim(ymin - 1, ymax + 1)     # márgenes

    # 4. Dibujar polígonos de fondo
    dibujar_poligonos(ax, lista_poligonos)

    # 5. Mostrar la ventana sin bloquear el script
    plt.show(block=False)

    # 6. Entrar en un REPL interactivo para poder
    #    añadir o modificar datos “sobre la marcha”
    try:    
        from code import interact
        interact(local=globals())
    finally:
        # Si hay curvas en el diccionario dedicado a guardarlas, se escriben los datos en un fichero
        if len(curvas_guardar_dict) > 0:
            if ruta_archivo_curvas == "":
                nombre_poligono = os.path.basename(ruta_poligono)
                nombre_sin_ext = os.path.splitext(nombre_poligono)[0]
                base = "./curvas_" + nombre_sin_ext
            else:
                base = ruta_archivo_curvas

            if base[-5:] != ".json":
                base += ".json"
            
            ruta_archivo_curvas = base
            if not sobreescribir:
                i = 1
                while os.path.exists(ruta_archivo_curvas):
                    ruta_archivo_curvas = f"{base[:-5]}_{i}.json"
                    i += 1
            
            guardar_dict_en_archivo(ruta_archivo_curvas, curvas_guardar_dict)
            print(f"Curvas guardadas en el fichero '{ruta_archivo_curvas}'")
