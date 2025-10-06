import numpy as np
import sympy as sp
import bisect
from ast import literal_eval
from Codigo.Auxiliares.hermite import hermite_nodos
t = sp.symbols('t')

class Nodo1d(object):
    def __init__(self, tiempo, valor, derivadas = []):
        self.tiempo = sp.Rational(tiempo)
        self.valor = sp.Rational(valor)
        self.derivadas = [sp.Rational(d) for d in derivadas]
    
    def get_tiempo(self):
        return self.tiempo
    
    def get_valor(self):
        return self.valor
    
    def get_derivadas(self):
        return self.derivadas
    
    def set_tiempo(self, t):
        self.tiempo = sp.Rational(t)

    def set_valor(self, v):
        self.valor = sp.Rational(v)

    def set_derivadas(self, der_list):
        self.derivadas = [sp.Rational(d) for d in der_list]
    
    @classmethod
    def from_dict(cls, datos):
        """
        Construye un nodo a partir de un diccionario datos, que debe incluir las claves "tiempo", "valor" y "derivadas".
        Los valores se convierten a objetos sympy.Rational.
        """
        tiempo = datos["tiempo"]
        valor = datos["valor"]
        derivadas = datos["derivadas"]
        return cls(tiempo, valor, derivadas)
    
    def to_dict(self):
        """
        Devuelve un diccionario con los datos del nodo, incluyendo tiempo, valor y derivadas.
        Los valores se convierten a cadenas para poder almacenarlos en un fichero.
        """
        tiempo = str(self.tiempo)
        valor = str(self.valor)
        derivadas = [str(d) for d in self.derivadas]
        return {
            "tiempo": tiempo,
            "valor": valor,
            "derivadas": derivadas
        }
    
    def __str__(self):
        return f"Tiempo: {self.tiempo}\n" + f"Valor: {self.valor}\n" + f"Derivadas: {self.derivadas}\n"

class PolinomioInterpolacion(object):
    def __init__(self, lista_nodos, polinomio = None):
        self.nodos = lista_nodos
        self.nodos.sort(key = lambda n: n.get_tiempo())
        self.tiempos = [ n.get_tiempo() for n in self.nodos ]
        self.poly = polinomio

    @classmethod
    def from_dict(cls, datos):
        """
        Construye el polinomio a partir de un diccionario datos, que debe incluir una lista de nodos
        dados en forma de diccionario. También incluye la expresión del polinomio, que podría ser None.
        """

        nodos_dict_list = datos["nodos"]
        nodos = [ Nodo1d.from_dict(n) for n in nodos_dict_list ]

        poly = datos["poly"]

        if poly is None:
           pass
        else:
            poly = sp.Poly(poly, t)

        return cls(nodos, poly)
    
    def to_dict(self):
        """
        Devuelve un diccionario con los datos del polinomio, incluyendo una lista de nodos
        """
        
        nodos_dict_list = [ n.to_dict() for n in self.nodos ]
        if self.poly is None:
            poly = None
        else:
            poly = str(self.poly.as_expr())
        return {
            "nodos": nodos_dict_list,
            "poly": poly
        }

    def interpolar(self):
        self.poly = hermite_nodos(self.nodos)
    
    def evaluar(self, t0):
        if self.poly is None:
            raise Exception("No se puede evaluar. No hay polinomio interpolado.")
        return self.poly(t0)
    
    def actualizar_tiempos(self):
        self.tiempos = [n.get_tiempo() for n in self.nodos]
    
    def graficar(self, ax, color_grafica = 'blue', color_puntos = 'black', t0=None, t1=None, samples = 400):
        # Crear la lista de tiempos entre los que se debe dibujar la curva
        tiempos_grafica = list()
        if not t0 is None:
            tiempos_grafica.append(t0)
        tiempos_grafica.extend(self.tiempos)
        if not t1 is None:
            tiempos_grafica.append(t1)
        
        if self.poly is None:
            raise Exception("No se puede graficar un polinomio no interpolado")
        for i in range(len(tiempos_grafica) - 1):
            t_vals = np.linspace(tiempos_grafica[i], tiempos_grafica[i+1], samples)
            y_vals = np.array([self.poly(tj) for tj in t_vals])

            ax.plot(t_vals, y_vals, color = color_grafica)
        
        ax.scatter([n.get_tiempo() for n in self.nodos], [n.get_valor() for n in self.nodos],
                    color = color_puntos)
    
    def poner_nodo(self, nodo):
        """
        Añade un nodo al polinomio. Si el tiempo del nodo ya existe, lanza una Exception.
        """
        if not isinstance(nodo, Nodo1d):
            raise TypeError("El nodo debe ser una instancia de la clase Nodo")
        
        if nodo.get_tiempo() in self.tiempos:
            raise Exception(f"Ya existe un nodo con tiempo t = {nodo.get_tiempo()} en la curva")
        
        # Añadir nodo y reordenar según tiempos
        self.nodos.append(nodo)
        self.nodos.sort(key = lambda n: n.get_tiempo())
        self.actualizar_tiempos()

    def crear_nodo(self, t, valor, derivadas = []):
        nuevo_nodo = Nodo1d(t, valor, derivadas)
        index = bisect.bisect_left(self.tiempos, t)
        if index < len(self.tiempos) and self.tiempos[index] == t:
            print(f"El valor t = {t} ya tiene un nodo en esta curva. ¿Cómo desea proceder?")
            s = input("reemplazar (r) / modificar (m) / desplazar (d)").lower()
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
        self.actualizar_tiempos()

    def quitar_nodo(self, index):
        nodo = self.nodos.pop(index)
        self.tiempos.pop(index)
        print(f"Nodo {index} correspondiente a t = {nodo.get_tiempo()}, f(t) = {nodo.get_valor()} eliminado.")

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
                raise Exception("El valor de t introducido no es válido. Puede ser entero, decimal, o una fracción entrecomillada")

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
        
    def modificar_valor(self, index, valor_nuevo = None):
        """
        Modifica el valor impuesto en el nodo que ocupa la posición 'index'.
        Si no se ha especificado un valor nuevo, se pregunta al usuario.
        """ 
        nodo = self.nodos[index]  
        print(f"Modificando el nodo en tiempo t = {nodo.get_tiempo()}")
        print(f"Valor actual: {nodo.get_valor()}")

        # Si no se ha especificado punto, obtener un valor mediante input
        if valor_nuevo is None:
            try:
                valor_nuevo = sp.Rational(input("Introduce el nuevo valor para el nodo: "))
            except:
                raise Exception("Debe introducirse un valor numérico admisible. Por ejemplo: '1', '1.1' o '2/3'.")
        
        nodo.set_valor(valor_nuevo)
        print(f"Valor modificado. Nuevo valor {nodo.get_valor()}")
        return

    def modificar_derivadas(self, index, ders_nuevas = None):
        """
        Modifica las derivadas impuestas en el nodo que ocupa la posición 'index'
        Si no se han especificado las derivadas nuevas, pregunta al usario.
        """

        nodo = self.nodos[index]
        if ders_nuevas is None:
            print(f"Modificando derivadas en tiempo t = {nodo.get_tiempo()}")
            print(f"Valor f(t) = {nodo.get_valor()}")

            print(f"Derivadas en dicho punto actualmente: ")
            print(nodo.get_derivadas())

            try:
                ders_nuevas = literal_eval( 
                    "[" + input(f"Introduce nuevas derivadas en t = {nodo.get_tiempo()}," \
                    "\nseparadas por comas                : ") + "]")
            except:
                raise Exception("Error al leer las derivadas. Deben introducirse valores numéricos como 1, 1.1" \
                                "\nPara fracciones, escribirlas entrecomilladas, e.g. '2/3'")
    
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
        if not self.poly is None:
            s += "Polinomio: " + str(self.poly.as_expr()) + "\n"

        for i, nodo in enumerate(self.nodos):
            s += f"--- Nodo {i} ---\n"
            s += str(nodo)
            if i < len(self.nodos) - 1:
                s += "\n"

        return s
    
    def __repr__(self):
        return str(self)
    