import numpy as np
import sympy as sp
import bisect
from ast import literal_eval
from nodos import Nodo, punto_a_Rational
from hermite import curva_hermite_nodos
t = sp.symbols('t')

class Curva_Nodos(object):
    def __init__(self, lista_nodos, xpoly = None, ypoly = None):
        self.nodos = lista_nodos
        self.nodos.sort(key = lambda n: n.get_tiempo())
        self.tiempos = [n.get_tiempo() for n in self.nodos]
        self.xpoly = xpoly
        self.ypoly = ypoly

    @classmethod
    def from_dict(cls, datos):
        """
        Construye la curva a partir de un diccionario datos, que debe incluir una lista de nodos
        dados en forma de diccionario. También incluye los polinomios xpoly, ypoly, que podrían ser
        None.
        """

        nodos_dict_list = datos["nodos"]
        nodos = [Nodo.from_dict(n) for n in nodos_dict_list]

        xpoly = datos["xpoly"]
        ypoly = datos["ypoly"]

        if xpoly is None or ypoly is None:
           xpoly = ypoly = None
        else:
            xpoly = sp.Poly(xpoly, t)
            ypoly = sp.Poly(ypoly, t)

        return cls(nodos, xpoly, ypoly)
    
    def to_dict(self):
        """
        Genera un diccionario con los datos de la curva
        """
        nodos_dict_list = [n.to_dict() for n in self.nodos]
        if self.xpoly is None or self.ypoly is None:
            xpoly = ypoly = None
        else:
            xpoly = str(self.xpoly.as_expr())
            ypoly = str(self.ypoly.as_expr())
        return {
            "nodos": nodos_dict_list,
            "xpoly": xpoly,
            "ypoly": ypoly
        }

    def get_nodos(self):
        return self.nodos
    
    def actualizar_tiempos(self):
        self.tiempos = [n.get_tiempo() for n in self.nodos]

    def interpolar(self):
        self.xpoly, self.ypoly = curva_hermite_nodos(self.nodos)
    
    def evaluar(self, t0):
        return (self.xpoly(t0), self.ypoly(t0))
    
    def graficar(self, ax, color_curva = 'blue', color_puntos = 'black', samples = 400, t0=None, t1=None, puntos = True):
        """
        Dibuja la imagen de la curva en el intervalo dado por los nodos y, si se han proporcionado, 
        los tiempos t0 y t1.
        Devuelve los objetos correspondientes al dibujo de la curva y de los nodos en el gráfico
        (curva_graf y puntos_graf).
        """
        
        # Crear la lista de tiempos entre los que se debe dibujar la curva
        tiempos_grafica = list()
        if not t0 is None:
            tiempos_grafica.append(t0)
        tiempos_grafica.extend(self.tiempos)
        if not t1 is None:
            tiempos_grafica.append(t1)
        
        # Dibujar la curva en los intervalos dados
        x_vals = []
        y_vals = []
        for i in range(len(tiempos_grafica) - 1):
            t_vals = np.linspace(tiempos_grafica[i], tiempos_grafica[i+1], samples)

            x_vals.extend(np.array([self.xpoly(tj) for tj in t_vals]))
            y_vals.extend(np.array([self.ypoly(tj) for tj in t_vals]))

        curva_graf, = ax.plot(x_vals, y_vals, color = color_curva)

        # Dibujar los puntos correspondientes a los nodos
        puntos_graf = None
        if puntos:
            puntos_graf = ax.scatter([n.get_punto()[0] for n in self.nodos], [n.get_punto()[1] for n in self.nodos],
                    color = color_puntos)
        
        return curva_graf, puntos_graf

    def etiquetar_nodos(self, ax, color_puntos = 'black', color_texto = 'black', size_puntos = 10, fontsize=12, etiquetas_sec=False):
        """
        Marca los puntos de cada nodo en la gráfica y escribe a su lado el valor de t para el cual la curva pasa por el nodo
        """
        n = len(self.nodos) # numero de puntos
        textos = list()
        puntos_graf = ax.scatter([n.get_punto()[0] for n in self.nodos], [n.get_punto()[1] for n in self.nodos],
                    color = color_puntos, s=size_puntos)
        
        for i,n in enumerate(self.nodos):
            if etiquetas_sec:
                etiqueta = str(i)
            else:
                etiqueta = str(n.get_tiempo())
            textos.append(ax.text(n.get_punto()[0], n.get_punto()[1], etiqueta, fontsize=fontsize, color=color_texto))

        return puntos_graf, textos

    def poner_nodo(self, nodo):
        """
        Añade un nodo a la curva. Si el tiempo del nodo ya existe, lanza una Exception.
        """
        if not isinstance(nodo, Nodo):
            raise TypeError("El nodo debe ser una instancia de la clase Nodo")
        
        if nodo.get_tiempo() in self.tiempos:
            raise Exception(f"Ya existe un nodo con tiempo t = {nodo.get_tiempo()} en la curva")
        
        # Añadir nodo y reordenar según tiempos
        self.nodos.append(nodo)
        self.nodos.sort(key = lambda n: n.get_tiempo())
        self.actualizar_tiempos()

    def crear_nodo(self, t, punto, derivadas = None):
        """
        Crea un nodo con los parámetros proporcionados y lo añade a la curva.
        Si ya hay un nodo en la curva con el tiempo dado, pregunta al usuario.
        """
        t = sp.Rational(t)
        nuevo_nodo = Nodo(t, punto, derivadas)
        index = bisect.bisect_left(self.tiempos, t)
        if index < len(self.tiempos) and self.tiempos[index] == t:
            print(f"El valor t = {t} ya tiene un nodo en esta curva. ¿Cómo desea proceder?")
            s = input("reemplazar (r) / modificar (m) / desplazar (d)")
            if s == 'r' or s == 'reemplazar':
                self.nodos[index] = nuevo_nodo
            
            elif s == 'd' or s == 'desplazar':
                self.nodos.insert(index, nuevo_nodo)
                print(f"Nuevo nodo insertado en la posición {index}. Se modifican los nodos posteriores.")
                for i in range(index + 1, len(self.nodos)):
                    self.nodos[i].set_tiempo(self.nodos[i].get_tiempo() + 1)

            elif s == 'm' or s == 'modificar':
                self.nodos.insert(index, nuevo_nodo)
                print(f"Nuevo nodo insertado en la posición {index}. Se modifican los nodos posteriores.")
                for i in range(index + 1, len(self.nodos)):
                    nodo = self.nodos[i]
                    print(f"Nodo número {i}.\nPunto: {nodo.get_punto()}\nDerivadas: {nodo.get_derivadas()}")
                    try:
                        nodo.set_tiempo(input("Introduce el nuevo tiempo para este nodo: "))
                    except:
                        raise Exception("El valor introducido no es válido")
            
            else:
                raise Exception
            
        else:
            self.nodos.insert(index, nuevo_nodo)

        # Reordenar nodos y actualizar lista de tiempos
        self.nodos.sort(key = lambda n: n.get_tiempo())
        self.tiempos = [n.get_tiempo() for n in self.nodos]

    def quitar_nodo(self, index):
        """
        Elimina el nodo en la posición 'index'.
        """
        nodo = self.nodos.pop(index)
        self.tiempos.pop(index)
        print(f"Nodo {index} correspondiente a t = {nodo.get_tiempo()}, p = {nodo.get_punto()} eliminado.")

    def modificar_nodo(self,index):
        """
        Modifica el nodo cuyo índice en la lista es index.
        Pregunta al usuario para obtener sus nuevos valores para tiempo, punto y derivadas.
        """
        nodo = self.nodos[index]

        # Modificar el tiempo en el que pasa por el nodo
        print(f"Modificando el siguiente nodo:")
        print(nodo)
        try:
            t_nuevo = sp.Rational(input("Introduce el nuevo valor de t: "))
            if t_nuevo in self.tiempos and t_nuevo != nodo.get_tiempo():
                print("El tiempo especificado corresponde a un nodo ya existente. " \
                "Usa el método poner_nodo para añadir un nodo con dicho tiempo y modificar o reemplazar el existente")
                return
            nodo.set_tiempo(t_nuevo)
            print(f"Tiempo modificado. Nuevo valor t = {t_nuevo}")
        except:
            raise Exception
        
        # Modificar el valor del punto
        try:
            p_nuevo = literal_eval(input("Introduce el nuevo valor del punto: "))
            if not type(p_nuevo) is tuple:
                raise Exception("El punto debe escribirse como una tupla (x, y)")
            
            nodo.set_punto(p_nuevo)
            print(f"Punto modificado. Nuevo valor p = {punto_a_Rational(p_nuevo)}")
        except:
            raise Exception("El punto debe escribirse como una tupla (x, y)")
        
        # Modificar las derivadas en el nodo
        print(f"Derivadas actuales en este nodo: {nodo.get_derivadas()}")
        try:
            ders_nuevas = literal_eval("[" + input("Introduce las nuevas derivadas en el nodo, separadas por comas:\n") + "]")
            nodo.set_derivadas(ders_nuevas)
        except:
            raise Exception("Error al leer las derivadas. Deben escribirse como tuplas separadas por comas, " \
            "por ejemplo:\n'(0,2), (1,1), (3,-1)'")
        
        # Reordenar los nodos con respecto a su tiempo y actualizar lista de tiempos:
        self.nodos.sort(key = lambda n: n.get_tiempo())
        self.tiempos = [ n.get_tiempo() for n in self.nodos ]
        return

    def modificar_tiempo(self, index, t_nuevo = None):
        """
        Modifica el tiempo del nodo en el índice 'index'.
        Devuelve el nuevo índice del nodo tras la modificación.
        """
        nodo = self.nodos[index]

        # Obtener valor de t si no se ha especificado.
        if t_nuevo is None:
            print(f"Modificando el nodo en t = {nodo.get_tiempo()}")
            try:
                t_nuevo = sp.Rational(input("Introduce el nuevo valor de t: "))

            except:
                raise Exception("El valor de t introducido no es válido. Puede ser entero, decimal, o una fracción *sin* comillas")

        if t_nuevo in self.tiempos and t_nuevo != nodo.get_tiempo():
            raise Exception("El tiempo especificado corresponde a un nodo ya existente.")
        
        # Modificar el tiempo del nodo
        nodo.set_tiempo(t_nuevo)
        print(f"Tiempo modificado. Nuevo valor t = {nodo.get_tiempo()}")

        # Reordenar los nodos y actualizar tiempos
        self.nodos.sort(key = lambda n: n.get_tiempo())
        indice_nuevo = self.nodos.index(nodo)
        self.actualizar_tiempos()
        return indice_nuevo
        
    def modificar_punto(self, index, punto_nuevo = None):
        """
        Modifica el punto del nodo en el índice 'index'
        """
        nodo = self.nodos[index]  
        print(f"Modificando el nodo en tiempo t = {nodo.get_tiempo()}")
        print(f"Punto actual: {nodo.get_punto()}")

        # Si no se ha especificado punto, obtener un valor mediante input
        if punto_nuevo is None:
            try:
                punto_nuevo = literal_eval(input("Introduce el nuevo valor del punto: "))
                if not type(punto_nuevo) is tuple:
                    raise Exception("El punto debe escribirse como una tupla (x, y)")
            except:
                raise Exception("El punto debe escribirse como una tupla (x, y)")
        
        nodo.set_punto(punto_nuevo)
        print(f"Punto modificado. Nuevo valor {nodo.get_punto()}")
        return

    def modificar_derivadas(self, index, ders_nuevas = None):
        """
        Modifica las derivadas del nodo en el índice 'index'
        """
        nodo = self.nodos[index]
        if ders_nuevas is None:
            print(f"Modificando derivadas en tiempo t = {nodo.get_tiempo()}")
            print(f"Punto p = {nodo.get_punto()}")

            print(f"Derivadas en dicho punto actualmente: ")
            print(nodo.get_derivadas())

            try:
                ders_nuevas = literal_eval( 
                    "[" + input(f"Introduce nuevas derivadas en t = {nodo.get_tiempo()}," \
                    "\nseparadas por comas                : ") + "]")
            except:
                raise Exception("Error al leer las derivadas")
    
        nodo.set_derivadas(ders_nuevas)
        print(f"Derivadas modificadas. Nuevo valor {nodo.get_derivadas()}")
    
    def modificar_nodo(self, index, t_nuevo = None, punto_nuevo = None, ders_nuevas = None):
        """
        Para modificar los parámetros del nodo en el índice 'index'.
        Si no se han especificado, pregunta al usuario por nuevos valores 
        para el tiempo, el punto y las derivadas.
        Devuelve el nuevo índice del nodo.
        """

        indice_nuevo = self.modificar_tiempo(index, t_nuevo)
        self.modificar_punto(indice_nuevo, punto_nuevo)
        self.modificar_derivadas(indice_nuevo, ders_nuevas)

        return indice_nuevo

    def __str__(self):
        s = ""
        if (not self.xpoly is None) and (not self.ypoly is None):
            s += "Primera coordenada: " + str(self.xpoly.as_expr()) + "\n"
            s += "Segunda coordenada: " + str(self.ypoly.as_expr()) + "\n"

        for i, nodo in enumerate(self.nodos):
            s += f"--- Nodo {i} ---\n"
            s += str(nodo)
            if i < len(self.nodos) - 1:
                s += "\n"

        return s
    
    def __repr__(self):
        return str(self)
    