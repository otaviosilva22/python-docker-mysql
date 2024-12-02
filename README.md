# Aplicação CRUD em Python

Simples exemplo de backend para CRUD desenvolvido com Python e várias outras ferramentas.

## Tecnologias utilizadas:

- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [MySQL](https://www.mysql.com/)
- [Flask](https://flask.palletsprojects.com/en/stable/)

## 🚀 Como iniciar:

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

Instale as dependências:

```
pip install -r requirements.txt
```

## Como testar:

```bash
http://127.0.0.1:5000/user [POST, GET, PATCH e DELETE]
```

```json
POST & PATCH
{
    "username": "teste",
    "email": "email@mail.com"
}
```

```json
GET
http://127.0.0.1:5000/user?id=<id_usuario>
```

```json
DELETE
http://127.0.0.1:5000/user/<id>
```

## Autor:

Otávio Silva

[![Linkedin Badge](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/otaviosilva22/)](https://www.linkedin.com/in/otaviosilva22/)
[![Gmail Badge](https://img.shields.io/badge/-Gmail-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:otavio.ssilva22@gmail.com)](mailto:otavio.ssilva22@gmail.com)