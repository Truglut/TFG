# TFG: *Cómo deformar polinómicamente la bola unidad cerrada para construir poliedros*
Este repositorio contiene el código desarrollado para mi Trabajo de Fin de Grado en Matemáticas, presentado en julio de 2025.

Este proyecto explora cómo deformar polinómicamente la bola unidad tridimensional para obtener figuras poliédricas.
Implementa los métodos descritos en la memoria del TFG, combinando interpolación de Hermite, visualización y animación con Python.

---

## Contenidos

- [`memoria.pdf`](./memoria.pdf): memoria completa del trabajo.  
- [`Animaciones/`](./Animaciones): animaciones generadas para visualizar las transformaciones.  
- [`Codigo/`](./Codigo): código fuente dividido en módulos.  

---

## Estructura del código

El código se organiza en varios módulos:

- **Auxiliares** - funciones de soporte:
  - `graficas.py`: funciones para salidas gráficas.
  - `lectura_datos.py`: lectura de datos y preprocesamiento.
  - `hermite.py`: interpolación de Hermite.
  - `recta.py`, `cambios_signo.py`, `sturm.py`: comprobaciones técnicas y validación de resultados.
- **Curvas** - herramientas para construir curvas polinómicas interpolantes a un polígono dado.
  - `curvas_inter.py`: script principal (interfaz interactiva).
  - `nodos.py`, `clase_curva.py`: clases y estructuras de datos.
  - `DatosPoligonos/`: datos de ejemplo.
- **Polinomios** - funciones para interpolar valores y derivadas de polinomios univariados.
  - `repar_inter.py`: script principal.
  - `clase_polinomio.py`: definición de clases `Nodo1d` y `PolinomioInterpolacion`.
- **Animaciones** - generación y almacenamiento de animaciones del proceso.

---
## Ejecución
Los tres scripts principales son:

- `curvas_inter.py`
- `repar_inter.py`
- `animaciones_poligonos.py`

Para ejecutarlos desde la terminal, sitúate en el directorio principal del repositorio (`TFG`) y usa la sintaxis:

```bash
python -m TFG.Codigo.<Subcarpeta>.<nombre_script> <argumentos>
```

Por ejemplo:
```bash
python -m TFG.Codigo.Curvas.curvas_inter ./Codigo/Curvas/DatosPoligonos/octagono.json
```

### curvas_inter
---falta---

### repar_inter
---falta---

### animaciones_poligonos
---falta---

## Formato de datos
Los archivos de entrada se guardan en formato JSON. Por ejemplo, un archivo de polígonos tiene la forma:
```json
{
  "poligonos": [
    [[0, 0], [1, 0], [1, 1], [0, 1]]
  ]
}
```
Los archivos de curvas se guardan automáticamente al ejecutar la función `guardar_curva()` durante la ejecución de `curvas_inter`.
Los archivos de datos para animaciones tienen la forma:
```json
{
"poligonos": <poligonos>,
"curvas": [ <curva_1>, <curva_2>, ..., <curva_n>],
"reparametrizaciones": [<rep_1>, <rep_2>, ..., <rep_n>],
"tiempos": [t1, t2, ..., tm],
"tiempos_triangulos": [t_tri1, t_tri2, ..., t_tril]
}
```
donde 
- `<poligonos>` se introduce en el mismo formato que en los archivos de polígonos
- los datos de las curvas (`<curva_1>`, `<curva_2>`, etc.) en el formato generado por `guardar_curva()` de manera automática.
- `"reparametrizaciones"` es una lista de *strings* correspondientes a un polinomio de sympy en la variable 't'. Estos polinomios se asignarán como reparametrizaciones de las curvas introducidas en `"curvas"`, por orden.
- `"tiempos"` es una lista que contiene los extremos de los intervalos que se consideran en la animación
- `"tiempos_triangulos"` es una lista que contiene los tiempos para los cuales se dibuja un triángulo fijo en la animación.

## Requisitos
Son necesarias las siguientes librerías: `sympy`, `matplotlib`, `os`, `argparse`, `numpy`, `ast`, `json`, `bisect`.
```bash
pip install sympy matplotlib os argparse numpy ast json bisect
```
Se recomienda usar Python 3.10 o superior.

## Autoría
**Autor**: Andrés Contreras Santos <br>
**Supervisor**: José Francisco Fernando Galván <br>
**Universidad**: Universidad Complutense de Madrid (UCM) <br>
**Grado**: Matemáticas
**Año**: 2025
