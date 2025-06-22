def dibujar_poligonos(ax, lista_de_poligonos, colores = ['green', 'blue', 'red'], color_linea = 'black', alpha = 0.5):
    """
    Dibuja los poligonos de la lista sobre los ejes 'ax'.
    Cada polígono de la lista es una tupla con dos elementos. El primero es una tupla con la primera
    coordenada de cada uno de sus vértices, y el segundo es otra tupla con las segundas coordenadas.
    """
    if type(colores) == str:
        colores = [colores]
    n = len(colores)
    for i, tupla_vertices in enumerate(lista_de_poligonos):
        ax.fill(tupla_vertices[0], tupla_vertices[1], color = colores[i % n], alpha = alpha)
        ax.plot(tupla_vertices[0], tupla_vertices[1], color = color_linea, linewidth = 1)
    
    return