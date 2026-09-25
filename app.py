import os

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Las tareas viven en memoria mientras la aplicación está en ejecución.
# Cada tarea es un diccionario: {"id": int, "texto": str, "completada": bool, "prioridad": str}
tareas = []
siguiente_id = 1

# Orden en que se muestran las prioridades (menor número = va primero)
PRIORIDADES = {"alta": 0, "media": 1, "baja": 2}
FILTROS = ("todas", "pendientes", "completadas")


def volver_al_inicio():
    """Regresa a la página principal conservando el filtro que estaba activo."""
    filtro = request.form.get("filtro", "todas")
    if filtro not in FILTROS or filtro == "todas":
        return redirect(url_for("index"))
    return redirect(url_for("index", filtro=filtro))


@app.route("/")
def index():
    filtro = request.args.get("filtro", "todas")
    if filtro not in FILTROS:
        filtro = "todas"

    pendientes = sum(1 for t in tareas if not t["completada"])

    if filtro == "pendientes":
        visibles = [t for t in tareas if not t["completada"]]
    elif filtro == "completadas":
        visibles = [t for t in tareas if t["completada"]]
    else:
        visibles = tareas

    ordenadas = sorted(visibles, key=lambda t: PRIORIDADES[t["prioridad"]])
    return render_template(
        "index.html",
        tareas=ordenadas,
        total=len(tareas),
        pendientes=pendientes,
        filtro=filtro,
    )


@app.route("/agregar", methods=["POST"])
def agregar():
    global siguiente_id
    texto = request.form.get("texto", "").strip()
    prioridad = request.form.get("prioridad", "media")
    if prioridad not in PRIORIDADES:
        prioridad = "media"
    if texto:
        tareas.append({
            "id": siguiente_id,
            "texto": texto,
            "completada": False,
            "prioridad": prioridad,
        })
        siguiente_id += 1
    return volver_al_inicio()


@app.route("/completar/<int:tarea_id>", methods=["POST"])
def completar(tarea_id):
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            tarea["completada"] = not tarea["completada"]
            break
    return volver_al_inicio()


@app.route("/eliminar/<int:tarea_id>", methods=["POST"])
def eliminar(tarea_id):
    tareas[:] = [t for t in tareas if t["id"] != tarea_id]
    return volver_al_inicio()


if __name__ == "__main__":
    # El modo debug queda apagado por defecto; se activa con FLASK_DEBUG=1
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(port=3000, debug=debug)