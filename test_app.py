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

def test_agregar_con_prioridad(client):
    client.post("/agregar", data={"texto": "Urgente", "prioridad": "alta"})
    assert app_module.tareas[0]["prioridad"] == "alta"


def test_prioridad_invalida_usa_media(client):
    client.post("/agregar", data={"texto": "Algo", "prioridad": "rarisima"})
    assert app_module.tareas[0]["prioridad"] == "media"


def test_tareas_se_ordenan_por_prioridad(client):
    client.post("/agregar", data={"texto": "Tarea baja", "prioridad": "baja"})
    client.post("/agregar", data={"texto": "Tarea alta", "prioridad": "alta"})
    texto = client.get("/").get_data(as_text=True)
    assert texto.index("Tarea alta") < texto.index("Tarea baja")

def test_filtro_pendientes(client):
    client.post("/agregar", data={"texto": "Hecha"})
    client.post("/agregar", data={"texto": "Por hacer"})
    client.post("/completar/1")
    texto = client.get("/?filtro=pendientes").get_data(as_text=True)
    assert "Por hacer" in texto
    assert "Hecha" not in texto


def test_filtro_completadas(client):
    client.post("/agregar", data={"texto": "Hecha"})
    client.post("/agregar", data={"texto": "Por hacer"})
    client.post("/completar/1")
    texto = client.get("/?filtro=completadas").get_data(as_text=True)
    assert "Hecha" in texto
    assert "Por hacer" not in texto


def test_filtro_invalido_muestra_todas(client):
    client.post("/agregar", data={"texto": "Una"})
    client.post("/agregar", data={"texto": "Dos"})
    client.post("/completar/1")
    texto = client.get("/?filtro=inventado").get_data(as_text=True)
    assert "Una" in texto
    assert "Dos" in texto


def test_accion_conserva_el_filtro(client):
    client.post("/agregar", data={"texto": "Algo"})
    respuesta = client.post("/completar/1", data={"filtro": "pendientes"})
    assert respuesta.headers["Location"].endswith("/?filtro=pendientes")