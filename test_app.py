import pytest

import app as app_module


@pytest.fixture
def client():
    # Reinicia las tareas antes de cada prueba para que no se afecten entre sí
    app_module.tareas.clear()
    app_module.siguiente_id = 1
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


def test_pagina_principal_carga(client):
    respuesta = client.get("/")
    texto = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 200
    assert "Lista de tareas" in texto
    assert "No hay tareas todavía" in texto


def test_agregar_tarea(client):
    respuesta = client.post("/agregar", data={"texto": "Comprar leche"}, follow_redirects=True)
    assert respuesta.status_code == 200
    assert "Comprar leche" in respuesta.get_data(as_text=True)
    assert len(app_module.tareas) == 1


def test_no_agrega_tarea_vacia(client):
    client.post("/agregar", data={"texto": "   "})
    assert len(app_module.tareas) == 0


def test_completar_y_desmarcar_tarea(client):
    client.post("/agregar", data={"texto": "Estudiar"})
    client.post("/completar/1")
    assert app_module.tareas[0]["completada"] is True
    client.post("/completar/1")
    assert app_module.tareas[0]["completada"] is False


def test_eliminar_tarea_conserva_las_demas(client):
    client.post("/agregar", data={"texto": "Primera"})
    client.post("/agregar", data={"texto": "Segunda"})
    client.post("/eliminar/1")
    assert len(app_module.tareas) == 1
    assert app_module.tareas[0]["texto"] == "Segunda"


def test_id_inexistente_no_rompe_la_app(client):
    assert client.post("/completar/99").status_code == 302
    assert client.post("/eliminar/99").status_code == 302


def test_texto_con_html_se_muestra_como_texto(client):
    respuesta = client.post("/agregar", data={"texto": "<b>hola</b>"}, follow_redirects=True)
    texto = respuesta.get_data(as_text=True)
    assert "&lt;b&gt;hola&lt;/b&gt;" in texto
    assert "<b>hola</b>" not in texto

def test_contador_de_pendientes(client):
    client.post("/agregar", data={"texto": "Una"})
    client.post("/agregar", data={"texto": "Dos"})
    client.post("/completar/1")
    texto = client.get("/").get_data(as_text=True)
    assert "1 tarea pendiente de 2" in texto