import pytest
import json
from app import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_list_lesson_plans_empty(client):
    response = client.get("/api/lesson-plans")
    assert response.status_code == 200
    data = response.get_json()
    assert data["items"] == []
    assert data["pagination"]["total"] == 0


def test_create_lesson_plan(client):
    payload = {
        "title": "Introdução ao Python",
        "objective": "Ensinar fundamentos de programação Python",
        "summary": "Conceitos básicos de Python para iniciantes",
        "discipline": "Programação",
        "tags": ["python", "programação", "iniciantes"],
    }
    response = client.post(
        "/api/lesson-plans",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == payload["title"]
    assert data["discipline"] == payload["discipline"]
    assert "python" in data["tags"]


def test_create_lesson_plan_validation_error(client):
    payload = {"title": "AB"}  # Too short, missing required fields
    response = client.post(
        "/api/lesson-plans",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 422
    data = response.get_json()
    assert "errors" in data


def test_get_lesson_plan(client):
    payload = {
        "title": "Redes de Computadores",
        "objective": "Introduzir conceitos de redes",
        "summary": "OSI, TCP/IP e protocolos de rede",
        "discipline": "Redes",
    }
    create_resp = client.post(
        "/api/lesson-plans",
        data=json.dumps(payload),
        content_type="application/json",
    )
    plan_id = create_resp.get_json()["id"]

    response = client.get(f"/api/lesson-plans/{plan_id}")
    assert response.status_code == 200
    assert response.get_json()["title"] == payload["title"]


def test_update_lesson_plan(client):
    payload = {
        "title": "Aula de Álgebra",
        "objective": "Ensinar álgebra linear",
        "summary": "Vetores, matrizes e transformações",
        "discipline": "Matemática",
    }
    plan_id = client.post(
        "/api/lesson-plans",
        data=json.dumps(payload),
        content_type="application/json",
    ).get_json()["id"]

    update = {"title": "Álgebra Linear Avançada"}
    response = client.put(
        f"/api/lesson-plans/{plan_id}",
        data=json.dumps(update),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.get_json()["title"] == "Álgebra Linear Avançada"


def test_delete_lesson_plan(client):
    payload = {
        "title": "Para Deletar",
        "objective": "Testar deleção",
        "summary": "Plano de aula temporário",
        "discipline": "Teste",
    }
    plan_id = client.post(
        "/api/lesson-plans",
        data=json.dumps(payload),
        content_type="application/json",
    ).get_json()["id"]

    response = client.delete(f"/api/lesson-plans/{plan_id}")
    assert response.status_code == 200

    get_resp = client.get(f"/api/lesson-plans/{plan_id}")
    assert get_resp.status_code == 404


def test_filter_by_discipline(client):
    for discipline in ["Matemática", "Matemática", "Física"]:
        client.post(
            "/api/lesson-plans",
            data=json.dumps({
                "title": f"Aula de {discipline}",
                "objective": "Objetivo da aula",
                "summary": "Resumo da aula",
                "discipline": discipline,
            }),
            content_type="application/json",
        )

    response = client.get("/api/lesson-plans?discipline=Matemática")
    data = response.get_json()
    assert data["pagination"]["total"] == 2


def test_search_by_title(client):
    client.post(
        "/api/lesson-plans",
        data=json.dumps({
            "title": "Introdução ao OSPF",
            "objective": "Ensinar protocolo OSPF",
            "summary": "Roteamento dinâmico com OSPF",
            "discipline": "Redes",
        }),
        content_type="application/json",
    )

    response = client.get("/api/lesson-plans?search=OSPF")
    data = response.get_json()
    assert data["pagination"]["total"] == 1
    assert "OSPF" in data["items"][0]["title"]


def test_disciplines_endpoint(client):
    client.post(
        "/api/lesson-plans",
        data=json.dumps({
            "title": "Aula Teste",
            "objective": "Objetivo",
            "summary": "Resumo",
            "discipline": "Química",
        }),
        content_type="application/json",
    )
    response = client.get("/api/lesson-plans/disciplines")
    assert response.status_code == 200
    assert "Química" in response.get_json()
