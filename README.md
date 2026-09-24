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

## Uso
- Escribe una tarea en el campo de texto y presiona **Agregar**.
- Presiona **Completar** para marcar una tarea como hecha (se tacha). Puedes regresarla con **Desmarcar**.
- Presiona **Eliminar** para borrarla de la lista.

## Estructura del proyecto
```
lista-de-tareas/
├── app.py              # Servidor Flask y rutas
├── requirements.txt    # Dependencias
├── templates/
│   └── index.html      # Página principal
└── static/
    └── style.css       # Estilos
```

## Notas
Las tareas se guardan en memoria, así que se borran al detener el servidor.
La prueba indica que la base de datos es opcional y que basta con que los datos se mantengan mientras la aplicación está en ejecución.