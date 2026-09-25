# Lista de tareas
Aplicación web para administrar una lista de tareas.
Permite agregar tareas con prioridad, editarlas, marcarlas como completadas, eliminarlas y filtrarlas.
El backend está hecho en Python con Flask.

## Requisitos
- Python 3.10 o superior
- Git

## Instalación

1. Clona el repositorio:
```
   git clone https://github.com/ximena-serna/lista-de-tareas.git
   cd lista-de-tareas
```

2. Crea un entorno virtual:
```
   python -m venv venv
```

3. Activa el entorno virtual:
   - Windows (PowerShell): `venv\Scripts\activate`
   - macOS / Linux: `source venv/bin/activate`

4. Instala las dependencias:
```
   pip install -r requirements.txt
```

## Ejecución

```
python app.py
```

Abre en el navegador: http://localhost:3000

Para detener el servidor presiona `Ctrl + C`.

El modo debug está apagado por defecto. Para activarlo durante el desarrollo:
- Windows (PowerShell): `$env:FLASK_DEBUG="1"; python app.py`
- macOS / Linux: `FLASK_DEBUG=1 python app.py`

## Uso
- Escribe una tarea, elige su prioridad (alta, media o baja) y presiona **Agregar**. La lista se ordena de mayor a menor prioridad.
- Presiona **Completar** para marcar una tarea como hecha (se tacha). Puedes regresarla con **Desmarcar**.
- Presiona **Editar** para cambiar el texto o la prioridad de una tarea, y luego **Guardar** o **Cancelar**.
- Presiona **Eliminar** para borrarla de la lista.
- Usa los filtros **Todas**, **Pendientes** y **Completadas** para ver solo un grupo de tareas. El contador muestra cuántas quedan pendientes del total.

## Pruebas
Las pruebas automáticas usan pytest. Con el entorno virtual activo:

```
pip install -r requirements-dev.txt
pytest -v
```

Cubren agregar, completar, desmarcar, editar y eliminar tareas; el contador de pendientes; el orden por prioridad; los filtros; la validación de datos inválidos (texto vacío, prioridades o filtros que no existen, ids inexistentes) y que el HTML escrito en una tarea se muestre como texto.

## Estructura del proyecto
```
lista-de-tareas/
├── app.py                # Servidor Flask y rutas
├── test_app.py           # Pruebas automáticas
├── requirements.txt      # Dependencias para ejecutar la app
├── requirements-dev.txt  # Dependencias para correr las pruebas
├── templates/
│   └── index.html        # Página principal
└── static/
    └── style.css         # Estilos
```

## Decisiones técnicas
- Elegí Flask porque es ligero y para una aplicación de este tamaño no hacía falta algo más grande.
- Las tareas se guardan en una lista en memoria, ya que la prueba indica que la base de datos es opcional; por lo mismo, se borran al detener el servidor.
- Cada tarea tiene un id propio en lugar de identificarla por su posición en la lista. Así, al eliminar una tarea las demás conservan su identificador y los botones siguen apuntando a la tarea correcta.
- Las acciones de agregar, completar, editar y eliminar se envían con formularios POST y después redirigen a la página principal. Esto evita que una acción se repita si se recarga el navegador, y permite que la app funcione sin JavaScript. El filtro activo y la tarea que se está editando van en la URL, por eso después de cada acción regresas a la misma vista donde estabas.
- El backend valida todo lo que recibe: ignora texto vacío, usa prioridad media si llega un valor que no existe, muestra todas las tareas si el filtro no es válido y no falla si el id no existe. Aunque el formulario solo ofrezca opciones válidas, cualquiera puede mandar otros valores directo al servidor.
- El texto de las tareas se muestra con Jinja, que escapa el HTML automáticamente, así que si alguien escribe etiquetas o scripts se ven como texto y no se ejecutan.
- Separé las dependencias en dos archivos: `requirements.txt` solo tiene lo necesario para correr la app, y `requirements-dev.txt` agrega pytest para quien quiera correr las pruebas.

## Uso de inteligencia artificial
Usé Claude como apoyo durante todo el proyecto. Me ayudó a definir la estructura, generar el código por partes y resolver errores en la terminal. Construí la aplicación una funcionalidad a la vez, probando cada una en el navegador antes de hacer su commit, y al final cloné el repositorio en otra carpeta para confirmar que se podía levantar siguiendo solo este README. Después de tener la versión básica funcionando, decidí agregar pruebas automáticas, apagar el modo debug por defecto y sumar funciones que yo usaría en una lista de tareas: prioridad, filtros, edición y un contador de pendientes, cada una con sus propias pruebas.