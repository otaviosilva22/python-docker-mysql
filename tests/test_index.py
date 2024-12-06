import pytest
from src.app import app, db, User
from unittest.mock import MagicMock, patch

import sys
print("SYS PATH", sys.path)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as client:
            yield client
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python_user:admin@127.0.0.1:3306/python_database'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # with app.app_context():
    #     db.create_all() 
    # with app.app_context():
    #     yield app.test_client()
    # with app.app_context():
    #     db.session.remove()
    #     db.drop_all()

@patch('src.app.db.session.commit')
@patch('src.app.db.session.add')  
def test_create_user(mock_add, mock_commit, client):
   
    mock_add.return_valu = None
    mock_commit.return_value = None
    user_data = {
        'username': 'test_user',
        'email': 'test_user@example.com'
    }

    response = client.post("/user", json=user_data)
    assert response.status_code == 201

@patch('src.app.db.session.commit')
def test_create_user_failure(mock_commit, client):
    mock_commit.side_effect = Exception("Commit failed")
    user_data = {
        "username": "test_user",
        "email": "test_user@example.com"
    }

    response = client.post("/user", json=user_data)

    assert response.status_code == 500

@patch('src.app.db.session.commit')  # Mock do commit no banco
@patch('src.app.User.query')         # Mock do acesso ao banco via User.query
def test_update_user(mock_user_query, mock_commit, client):
    # Criando um mock para o usuário existente
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.username = 'old_user'
    mock_user.email = 'old_user@example.com'
    mock_user.to_json.return_value = {
        'id': 1,
        'ts': '2024-12-06T00:00:00',
        'username': 'updated_user',
        'email': 'updated_email@example.com'
    }

    # Configurando o mock para User.query.get retornar o usuário simulado
    mock_user_query.get.return_value = mock_user

    # Mock do commit no banco
    mock_commit.return_value = None

    # Dados para a requisição PATCH
    user_data = {
        'username': 'updated_user',
        'email': 'updated_email@example.com'
    }

    response = client.patch('/user/1', json=user_data)

    assert response.status_code == 200

@patch('src.app.User.query')         # Mock do acesso ao banco via User.query
def test_read_user(mock_query, client):
    # Mock da conexão com o banco
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.username = 'old_user'
    mock_user.email = 'old_user@example.com'
    mock_user.to_json.return_value = {
        'id': 1,
        'ts': '2024-12-06T00:00:00',
        'username': 'updated_user',
        'email': 'updated_email@example.com'
    }

    # Configurando o mock para User.query.get retornar o usuário simulado
    mock_query.get.return_value = mock_user

    # Faz a requisição GET
    response = client.get("/user?id=1")  # A URL agora usa um query parameter id=1

    assert response.status_code == 200

@patch('src.app.User.query')         # Mock do acesso ao banco via User.query
def test_read_user_not_found(mock_query, client):
    # Mock da conexão com o banco

    # Configurando o mock para User.query.get retornar o usuário simulado
    mock_query.get.return_value = None

    # Faz a requisição GET
    response = client.get("/user?id=1")  # A URL agora usa um query parameter id=1

    assert response.status_code == 404

@patch('src.app.db.session')
@patch('src.app.User.query')
def test_delete_user(mock_query_user, mock_session, client):
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.username = 'old_user'
    mock_user.email = 'old_user@example.com'
    mock_user.to_json.return_value = {
        'id': 1,
        'ts': '2024-12-06T00:00:00',
        'username': 'updated_user',
        'email': 'updated_email@example.com'
    }

    mock_query_user.get.return_value = mock_user
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None

    response = client.delete("/user?id=1")  # A URL agora usa um query parameter id=1

    # Verifica a resposta da API
    assert response.status_code == 200
