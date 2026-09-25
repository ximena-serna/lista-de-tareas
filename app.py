import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Las tareas viven en memoria mientras la aplicación está en ejecución.
# Cada tarea es un diccionario: {"id": int, "texto": str, "completada": bool}
tareas = []
siguiente_id = 1


@app.route("/")
def index():
    pendientes = sum(1 for t in tareas if not t["completada"])
    return render_template("index.html", tareas=tareas, pendientes=pendientes)


@app.route("/agregar", methods=["POST"])
def agregar():
    global siguiente_id
    texto = request.form.get("texto", "").strip()
    if texto:
        tareas.append({"id": siguiente_id, "texto": texto, "completada": False})
        siguiente_id += 1
    return redirect(url_for("index"))


@app.route("/completar/<int:tarea_id>", methods=["POST"])
def completar(tarea_id):
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            tarea["completada"] = not tarea["completada"]
            break
    return redirect(url_for("index"))


@app.route("/eliminar/<int:tarea_id>", methods=["POST"])
def eliminar(tarea_id):
    tareas[:] = [t for t in tareas if t["id"] != tarea_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(port=3000, debug=debug)