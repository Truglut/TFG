import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from matplotlib.patches import Polygon
from graficas import dibujar_poligonos
from lectura_datos import leer_datos_desde_json
from auxiliares_animacion import *

if __name__ == "__main__":
    print("Iniciando...")

    # 1. Parsear argumento de entrada (ruta al JSON)
    args = parsear_argumentos()
    parametros = leer_argumentos(args)
    
    # 2. Leer polígonos y curvas desde el JSON 
    ruta_datos = args.archivo_datos
    lista_poligonos, lista_curvas, intervalos_t, tiempos_triangulos, tiempos_triangulos_mal, \
    intervalos_triangulos_mal, reparametrizaciones = leer_datos_desde_json(ruta_datos)
    n = len(lista_curvas)
    print("Polígonos y curvas leídos")

    # Determinamos límites de la figura
    xmin = float(min(vx for poly in lista_poligonos for vx in poly[0]))
    xmax = float(max(vx for poly in lista_poligonos for vx in poly[0]))
    ymin = float(min(vy for poly in lista_poligonos for vy in poly[1]))
    ymax = float(max(vy for poly in lista_poligonos for vy in poly[1]))

    if len(tiempos_triangulos) == 0:
        tiempos_triangulos = intervalos_t

    # Reparametrización de las curvas dadas
    t_vals = crear_valores_t(intervalos_t, parametros["frames_por_intervalo"])
    t_vals_curvas = list()
    if not parametros["usar_repars"]:
        reparametrizaciones = []

    if len(reparametrizaciones) > 0:
        if len(reparametrizaciones) < n:
            print("Hay menos reparametrizaciones que curvas, se asignan en orden de aparición en el fichero")
        for i in range(min(len(reparametrizaciones), n)):
            t_vals_curvas.append(np.array([reparametrizaciones[i](t) for t in t_vals]))
    
    for i in range(n - len(reparametrizaciones)):
        t_vals_curvas.append(t_vals)
    
    # Cálculo del número de frames para que el tiempo sea el indicado
    frames_animacion = len(t_vals)
    tiempo_por_frame = parametros["tiempo_animacion"]/frames_animacion
    frames_fade_inicial = round(parametros["tiempo_fade_inicial"]/tiempo_por_frame)
    frames_parada_inicial = round(parametros["tiempo_parada_inicial"]/tiempo_por_frame)
    frames_parada_final = round(parametros["tiempo_parada_final"]/tiempo_por_frame)
    num_frames = frames_animacion + frames_parada_inicial + frames_parada_final + frames_fade_inicial
    tiempo_total = (parametros["tiempo_animacion"] + parametros["tiempo_parada_inicial"] + 
                    parametros["tiempo_parada_final"] + parametros["tiempo_fade_inicial"])

    
    # Evaluación de las curvas dadas en sus respectivos intervalos de tiempo
    x = []
    y = []
    for i in range(n):
        x.append(np.array([lista_curvas[i].xpoly(t) for t in t_vals_curvas[i]]))
        y.append(np.array([lista_curvas[i].ypoly(t) for t in t_vals_curvas[i]]))

    # Creamos la figura para la animación
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_axis_off()
    longitud_x = xmax - xmin
    longitud_y = ymax - ymin
    ax.set_xlim(xmin - 0.05*longitud_x, xmax + 0.05*longitud_x)
    ax.set_ylim(ymin - 0.05*longitud_y, ymax + 0.05*longitud_y)
    dibujar_poligonos(ax, lista_poligonos, colores=parametros["colores_poligonos"], alpha = parametros["alpha_figura"])

    # Crear los objetos que aparecen en la animación
    points = []
    for i in range(n):
        points.append(ax.plot([], [], marker='o', color='black')[0])

    traces_x = []
    traces_y = []
    traces = []

    colores_curvas = parametros["colores_curvas"]
    nro_colores_curvas = len(colores_curvas)
    for i in range(n):
        traces_x.append([])
        traces_y.append([])
        traces.append(ax.plot([], [], color = colores_curvas[i%nro_colores_curvas], alpha = parametros["alpha_curvas"])[0])

    colormap_poligono = plt.cm.winter
    verts_poligono_inicial = [(x[i][0], y[i][0]) for i in range(n)]
    poligono_movil = Polygon(verts_poligono_inicial, closed=True, color = colormap_poligono(0), alpha = 0)
    ax.add_patch(poligono_movil)

    edge_poligonos = parametros["edge_poligonos"]

    poligono_inicial = Polygon(verts_poligono_inicial, closed=True, 
                               facecolor = colormap_poligono(0), 
                               edgecolor = decidir_edgecolor(edge_poligonos, colormap_poligono(0)), alpha = 0)
    ax.add_patch(poligono_inicial)

    artists = points + traces + [poligono_movil] + [poligono_inicial]
    alpha_poligono_movil_ahora = 0
    alpha_poligono_inicial_ahora = 0
    def init():
        """
        Función que inicializa la animación.
        """
        global alpha_poligono_inicial_ahora
        global alpha_poligono_movil_ahora
        alpha_poligono_inicial_ahora = 0
        alpha_poligono_movil_ahora = 0

        # Borrar trazas de las curvas
        for l in traces_x:
            l.clear()
        for l in traces_y:
            l.clear()

        # Fijar los puntos  y el polígono a su posición inicial
        for i, point in enumerate(points):
            point.set_data([x[i][0]], [y[i][0]])

        poligono_movil.set_xy(verts_poligono_inicial)

        return artists

    # Cálculos relativos al comienzo de la animación
    # (entradas progresivas del polígono móvil y el polígono inicial)
    alpha_poligono_movil = parametros["alpha_poligono_movil"]
    alpha_poligonos_fijos = parametros["alpha_poligonos_fijos"]
    incremento_alpha_poligono = alpha_poligono_movil / frames_fade_inicial
    incremento_alpha_triangulo = alpha_poligonos_fijos / frames_fade_inicial
    alpha_poligono_movil_ahora = 0
    alpha_poligono_inicial_ahora = 0

    ult_frame = num_frames - frames_parada_final - 1
    frames_inicio = frames_fade_inicial + frames_parada_inicial
    def update(frame):
        """
        Función que actualiza la animación en cada frame.
        """
        global alpha_poligono_movil_ahora
        global alpha_poligono_inicial_ahora
        global alpha_poligonos_fijos
        if frame < frames_inicio:
            if 0 < frame <= frames_fade_inicial: #animacion inicial - entrada progresiva de los polígonos
                if frame < frames_fade_inicial:
                    alpha_poligono_movil_ahora += incremento_alpha_poligono
                    alpha_poligono_inicial_ahora += incremento_alpha_triangulo
                    poligono_movil.set_alpha(alpha_poligono_movil_ahora)
                    poligono_inicial.set_alpha(alpha_poligono_inicial_ahora)
                if frame == frames_fade_inicial:
                    poligono_movil.set_alpha(alpha_poligono_movil)
                    poligono_inicial.set_alpha(alpha_poligonos_fijos)
            return artists
        
        if frame > ult_frame:
            return artists
        
        t = frame - frames_inicio   #tiempo actual en la animación

        #Actualizar los objetos
        for i, point in enumerate(points):
            point.set_data([x[i][t]], [y[i][t]])
        
        for i, trace_x in enumerate(traces_x):
            trace_x.append(x[i][t])
        for i, trace_y in enumerate(traces_y):
            trace_y.append(y[i][t])

        for i, trace in enumerate(traces):
            trace.set_data(traces_x[i], traces_y[i])

        verts_poligono_movil = [(x[i][t], y[i][t]) for i in range(n)]
        poligono_movil.set_xy(verts_poligono_movil)

        color_interior = colormap_poligono(t/frames_animacion)
        if any(intervalo[0] < t_vals[t] < intervalo[1] for intervalo in intervalos_triangulos_mal):
            poligono_movil.set_color('red')
        else:    
            poligono_movil.set_color(color_interior)

        # Para los valores clave de t, ponemos un triangulo
        if t!= 0 and t_vals[t] in tiempos_triangulos:
            nuevo_poligono = Polygon(verts_poligono_movil, closed=True, facecolor = color_interior, 
                                     edgecolor = decidir_edgecolor(edge_poligonos, color_interior), 
                                     alpha = alpha_poligonos_fijos)
            artists.append(nuevo_poligono)
            ax.add_patch(nuevo_poligono)

        if t_vals[t] in tiempos_triangulos_mal:
            nuevo_poligono = Polygon(verts_poligono_movil, closed=True, facecolor = 'red', 
                                     edgecolor = None, alpha = alpha_poligonos_fijos)
            artists.append(nuevo_poligono)
            ax.add_patch(nuevo_poligono)
            return artists
    
        return artists
    
        
    
    ani = FuncAnimation(fig, update, init_func=init, frames=num_frames, interval = tiempo_total/num_frames, blit=True)
    
    # Guardar animación como GIF
    if parametros["guardar"]:
        ruta_archivo = parametros["ruta_archivo"]
        base, extension = os.path.splitext(ruta_archivo)
        tiempo_total_segundos = tiempo_total/1000
        fps = round(num_frames/tiempo_total_segundos)
        print(f"Guardando con {fps} fps")

        i = 0
        while os.path.exists(ruta_archivo):
            i += 1
            ruta_archivo = f"{base}_{i}" + extension

        if extension == ".gif":
            writer = PillowWriter(fps=fps)
        elif extension == ".mp4":         
            writer = FFMpegWriter(fps=fps, metadata=dict(artist='Andrés Contreras Santos'), bitrate=2500)

        ani.save(ruta_archivo, writer=writer, dpi=125)
        print(f"Animación guardada como {ruta_archivo}")
    else:
        plt.show()