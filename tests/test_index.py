import pytest
from unittest.mock import patch, MagicMock
from src.index import app, UseDatabase

import sys
print("SYS PATH", sys.path)


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch("src.index.UseDatabase")
def test_create_user(mock_db, client):
    # Mock da conexão com o banco
    mock_cursor = MagicMock()
    mock_db.return_value.__enter__.return_value = mock_cursor

    # Dados enviados no corpo da requisição
    user_data = {
        "username": "test_user",
        "email": "test_user@example.com"
    }

    # Simula o comportamento do cursor.execute()
    mock_cursor.execute.return_value = 1

    # Faz a requisição POST
    response = client.post("/user", json=user_data)

    # Verifica se o banco foi chamado com os dados corretos
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO users (username, email) VALUES (%s, %s)",
        ("test_user", "test_user@example.com")
    )

    # Verifica a resposta da API
    assert response.status_code == 201
    assert response.get_json() == {"created": True}

@patch("src.index.UseDatabase")
def test_create_user_failure(mock_db, client):
    # Mock da conexão com o banco que lança um erro
    mock_cursor = MagicMock()
    mock_db.return_value.__enter__.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Database error")

    # Dados enviados no corpo da requisição
    user_data = {
        "username": "test_user",
        "email": "test_user@example.com"
    }

    # Faz a requisição POST
    response = client.post("/user", json=user_data)

    # Verifica a resposta da API em caso de erro
    assert response.status_code == 500
    assert response.get_json()["created"] is False
    assert "error" in response.get_json()

@patch("src.index.UseDatabase")
def test_update_user(mock_db, client):
    # Mock da conexão com o banco
    mock_cursor = MagicMock()
    mock_db.return_value.__enter__.return_value = mock_cursor

    # Dados enviados no corpo da requisição
    user_data = {
        "username": "test_user",
        "email": "test_user@example.com"
    }

    # Simula o comportamento do cursor.execute()
    mock_cursor.execute.return_value = 1

    # Faz a requisição POST
    response = client.patch("/user/1", json=user_data)

    # Verifica se o banco foi chamado com os dados corretos
    mock_cursor.execute.assert_called_once_with(
        """UPDATE users SET username = %s, email = %s  WHERE id = %s""",
        ("test_user", "test_user@example.com", '1')
    )

    # Verifica a resposta da API
    assert response.status_code == 200
    assert response.get_json() == {"update": True}

@patch("src.index.UseDatabase")
def test_read_user(mock_db, client):
    # Mock da conexão com o banco
    mock_cursor = MagicMock()
    mock_db.return_value.__enter__.return_value = mock_cursor    

    # Simula o comportamento do cursor.execute() e fetchall()
    mock_cursor.execute.return_value = None  # Não precisamos simular a execução, só a consulta
    mock_cursor.fetchall.return_value = [
        (1, "", "test_user", "test_user@example.com")
    ]  # Dados simulados retornados pela consulta

    # Faz a requisição GET
    response = client.get("/user?id=1")  # A URL agora usa um query parameter id=1

    # Verifica se o banco foi chamado com os dados corretos
    mock_cursor.execute.assert_called_once_with(
        """SELECT * FROM users WHERE id = %s""",
        ('1',)  # Passando o id como parâmetro corretamente
    )

    
    # Verifica a resposta da API
    assert response.status_code == 200
    assert response.get_json() == {
        "read": True,
        "result": [
            {"id": 1, "username": "test_user", "email": "test_user@example.com"}
        ]
    }

@patch("src.index.UseDatabase")
def test_delete_user(mock_db, client):
    # Mock da conexão com o banco
    mock_cursor = MagicMock()
    mock_db.return_value.__enter__.return_value = mock_cursor    

    # Simula o comportamento do cursor.execute() sem usar fetchall()
    mock_cursor.execute.return_value = None  # Não precisamos simular a execução, só a consulta

    # Faz a requisição DELETE com o parâmetro id=1
    response = client.delete("/user?id=1")

    # Verifica se o banco foi chamado com os dados corretos
    mock_cursor.execute.assert_called_once_with(
        """DELETE FROM users WHERE id = %s""",
        ('1',)  # Passando o id como parâmetro corretamente
    )

    # Verifica a resposta da API
    assert response.status_code == 200
    assert response.get_json() == {"deleted": True}
