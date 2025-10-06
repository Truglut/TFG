# TFG: *Cómo deformar polinómicamente la bola unidad cerrada para construir poliedros*
Este repositorio contiene el código desarrollado para mi Trabajo de Fin de Grado en Matemáticas, presentado en julio de 2025.

El proyecto explora cómo deformar polinómicamente la bola unidad tridimensional para obtener figuras poliédricas.
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
`curvas_inter.py` es la interfaz interactiva para generar y editar curvas polinómicas de interpolación que reproducen un polígono dado. Lee un fichero JSON con los polígonos a representar, dibuja la(s) figura(s) y abre un REPL interactivo donde el usuario puede crear/editar nodos y calcular la interpolación de Hermite empleando las clases CurvaInterpolacion y Nodo. El script también admite cargar curvas ya calculadas desde un JSON y permite guardar en disco las curvas creadas durante la sesión.

Argumentos:
- `archivo_poligonos` (posición): ruta al fichero JSON que contiene los polígonos a mostrar.
- `--archivo_curvas` (opcional): ruta a un JSON con curvas ya calculadas (se cargan en memoria).

### repar_inter
`repar_inter.py` es la herramienta interactiva para construir polinomios univariantes que interpolan valores y derivadas en tiempos dados (interpolación de Hermite en 1D). El usuario introduce los tiempos y los datos (valor en cada tiempo y derivadas) por consola; el script construye un objeto `PolinomioInterpolacion` y muestra su gráfica, permitiendo entrar en un REPL para editar nodos y volver a interpolar. El polinomio y los nodos pueden guardarse en formato JSON al cerrar la sesión. 

No toma argumentos en línea de comandos.

### animaciones_poligonos
`animacion_poligonos.py` genera animaciones (GIF/MP4/AVI o visualización en pantalla) que muestran cómo un polígono “se deforma” siguiendo las curvas polinómicas definidas. Lee sus datos a partir de un fichero JSON. Toma argumentos en línea de comandos:
- `archivo_datos` (posición): fichero JSON con los datos para la animación (polígonos, curvas, intervalos, reparametrizaciones, etc.).
- Opcionales (pasados como --flag): `--frames_por_intervalo`, `--tiempo_animacion`, `--tiempo_fade_inicial`, `--tiempo_parada_inicial`, `--tiempo_parada_final`, `--reparametrizaciones`, `--colores_poligonos`, `--alpha_figura`, `--alpha_poligono_movil`, `--alpha_poligonos_fijos`, `--guardar_archivo`, `--colores_curvas`, `--alpha_curvas`, `--edge_poligonos`. (La función `leer_argumentos` aplica valores por defecto si no se pasan).

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
**Grado**: Matemáticas <br>
**Año**: 2025
