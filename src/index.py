from flask import Flask, render_template, request, jsonify, Response
from markupsafe import escape
import mysql.connector

app = Flask(__name__)

app.config['dbconfig'] = {
    'user': 'python_user',
    'password': 'admin',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'python_database'
}

class UseDatabase:
    def __init__(self, config: dict) -> None:
        self.configuration = config

    def __enter__(self) -> 'cursor':
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        _SQL = """CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            ts timestamp default current_timestamp,
            username varchar(128),
            email varchar(128)
        )"""
        self.cursor.execute(_SQL)
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

def create_table() -> None:
    

    return _SQL

@app.route('/')
def entry_page() -> Response:
    return jsonify({
        "Rotas": [
            'POST -> https://127.0.0.1/5000/user'
        ]
    })

@app.route('/user', methods=['POST'])
def create() -> Response:
    request_body = request.get_json()
    username = request_body.get('username')
    email = request_body.get('email')
    data = (username, email)
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:

            _SQL = """INSERT INTO users (username, email) VALUES (%s, %s)"""
            resultado = cursor.execute(_SQL, data)

            return jsonify({
                "created": True
            }), 201
    except Exception as err:
        print("Erro ao inserir dados: {err}")
        return jsonify({
            "created": False,
            "error": str(err)
        }), 500

@app.route('/user/<id>', methods=['PATCH'])
def update(id) -> Response:
    request_body = request.get_json()
    username = request_body.get('username')
    email = request_body.get('email')
    data = (username, email, id)
    _SQL = """UPDATE users SET username = %s, email = %s  WHERE id = %s"""
    try: 
        with UseDatabase(app.config['dbconfig']) as cursor:
            resultado = cursor.execute(_SQL, data)
            return jsonify({
                        "update": True
                    }), 200
    except Exception as err:
        return jsonify({
            "update": False,
            "error": str(err)
        }), 500

@app.route('/user', methods=['GET'])
def read() -> Response:
    query_param = request.args.get('id', '')
    data = (query_param,)
    _SQL = """SELECT * FROM users WHERE id = %s"""
    try: 
        with UseDatabase(app.config['dbconfig']) as cursor:
            cursor.execute(_SQL, data)
            result = cursor.fetchall()
            json_formated = []
            for row in result:
                json_formated.append({
                    "id": row[0],
                    "username": row[2],
                    "email": row[3]
                })

            return jsonify({
                        "read": True,
                        "result": json_formated
                    })
    except Exception as err:
        return jsonify({
            "read": False,
            "error": str(err)
        })

@app.route('/user', methods=['DELETE'])
def delete() -> Response:
    query_param = request.args.get('id', '')
    data = (query_param,)
    _SQL = """DELETE FROM users WHERE id = %s"""
    try: 
        with UseDatabase(app.config['dbconfig']) as cursor:
            cursor.execute(_SQL, data)
            result = cursor.fetchall()
            json_formated = []
            
            return jsonify({
                        "deleted": True,
                    })
    except Exception as err:
        return jsonify({
            "deleted": False,
            "error": str(err)
        })




if __name__ == '__main__':
    app.run(debug=True)