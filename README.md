# Lista de tareas
Aplicación web sencilla para administrar una lista de tareas.
Permite agregar tareas, marcarlas como completadas y eliminarlas.
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
- Escribe una tarea en el campo de texto y presiona **Agregar**.
- Presiona **Completar** para marcar una tarea como hecha (se tacha). Puedes regresarla con **Desmarcar**.
- Presiona **Eliminar** para borrarla de la lista.

## Pruebas
Las pruebas automáticas usan pytest. Con el entorno virtual activo:
```
pip install -r requirements-dev.txt
pytest -v
```
Revisan que la página cargue, que se agreguen tareas, que no se acepte texto vacío, que se puedan completar, desmarcar y eliminar, que un id inexistente no rompa la aplicación y que el HTML escrito en una tarea se muestre como texto.

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
- Las acciones de agregar, completar y eliminar se envían con formularios POST y después redirigen a la página principal. Esto evita que una acción se repita si se recarga el navegador, y permite que la app funcione sin JavaScript.
- El texto de las tareas se muestra con Jinja, que escapa el HTML automáticamente, así que si alguien escribe etiquetas o scripts se ven como texto y no se ejecutan.
- Separé las dependencias en dos archivos: `requirements.txt` solo tiene lo necesario para correr la app, y `requirements-dev.txt` agrega pytest para quien quiera correr las pruebas.

## Uso de inteligencia artificial
Usé Claude como apoyo durante todo el proyecto. Me ayudó a definir la estructura, generar el código por partes y resolver errores en la terminal. Construí la aplicación una funcionalidad a la vez, probando cada una en el navegador antes de hacer su commit, y al final cloné el repositorio en otra carpeta para confirmar que se podía levantar siguiendo solo este README. En el camino corregí algunos problemas, como un error de sangría al pegar código en Python y la creación del `.gitignore` desde PowerShell. Después de tener la app funcionando, decidí agregar pruebas automáticas y apagar el modo debug por defecto para mejorar la calidad de la entrega.