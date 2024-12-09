# Aplicação CRUD em Python

Simples exemplo de backend para CRUD desenvolvido com Python e várias outras ferramentas.

## Tecnologias utilizadas:

- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [MySQL](https://www.mysql.com/)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [PyTest](https://docs.pytest.org/en/stable/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Prometheus](https://prometheus.io/)

## 🚀 Como iniciar

Crie o ambiente virtual:

```bash
python3 -m venv venv
```

Inicie o ambiente virtual:

- Windows

```
.\venv\Scripts\activate
```

- Linux

```
source venv/bin/activate
```

Instale as dependências, inicie o docker e o projeto:

```bash
pip install -r requirements.txt
docker-compose up
python3 src/app.py
```

## Testes de integração (API):

```bash
http://127.0.0.1:5000/user [POST, GET, PATCH e DELETE]
```

- Body request (POST E PATCH):

```json
{
  "username": "teste",
  "email": "email@mail.com"
}
```

- URL param (GET):

```bash
http://127.0.0.1:5000/user?id=<id_usuario>
```

- PATH param (DELETE):

```bash
http://127.0.0.1:5000/user/<id>
```

## Testes unitários:

```bash
pytest
```

- Opção com coverage (métrica de cobertura de testes) no terminal:

```bash
pytest --cov=src --cov-report=term
```

- Opção com coverage gerando arquivo html:

```bash
pytest --cov=src --cov-report=html
```

## Métricas do Prometheus:

```bash
https://localhost:9090
```

- Acesso ao histórico de métricas do Pushgateway:

```bash
https://localhost:9091/metrics
```

## Autor:

Otávio Silva

[![Linkedin Badge](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/otaviosilva22/)](https://www.linkedin.com/in/otaviosilva22/)
[![Gmail Badge](https://img.shields.io/badge/-Gmail-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:otavio.ssilva22@gmail.com)](mailto:otavio.ssilva22@gmail.com)
