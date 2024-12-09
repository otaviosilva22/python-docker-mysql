from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python_user:admin@127.0.0.1:3306/python_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

registry = CollectorRegistry()

user_metric_success = Gauge('user_metric_success', 'Quantidade de usuários', registry=registry)
user_metric_success.set(0)

user_metric_error = Gauge('user_metric_error', 'Erros ao cadastrar usuário', registry=registry)
user_metric_error.set(0)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ts = db.Column(db.DateTime, server_default=db.func.now())
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def to_json(self):
        return {
            'id': self.id,
            'ts': self.ts,
            'username': self.username,
            'email': self.email
        }

@app.route('/user', methods=['POST'])
def create() -> Response:
    request_body = request.get_json()
    username = request_body.get('username')
    email = request_body.get('email')
    
    if not username or not email:
        
        user_metric_error.inc()
        push_to_gateway('localhost:9091', 'job=user_metric_error', registry=registry)
        return jsonify({
            'created': False,
            'error': 'Invalid params'
        }), 400


    try:
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()

        user_metric_success.inc()
        push_to_gateway('localhost:9091', 'job=user_metric_success', registry=registry)

        return jsonify({
            'created': True,
            'user': new_user.to_json()
        }), 201
    except Exception as err:
        user_metric_error.inc()
        push_to_gateway('localhost:9091', 'job=user_metric_error', registry=registry)
        print("Erro ao inserir dados: {err}")
        return jsonify({
            'created': False,
            'error': str(err)
        }), 500

@app.route('/user/<id>', methods=['PATCH'])
def update(id) -> Response:
    request_body = request.get_json()
    username = request_body.get('username')
    email = request_body.get('email')
    try: 
        update_user = User.query.get(id)

        if not update_user:
            return jsonify({'error': 'User not found'}), 404
        
        update_user.username = username
        update_user.email = email
        db.session.commit()

        return jsonify({
            'updated': True,
            'user': update_user.to_json()
        }), 200
    except Exception as err:
        return jsonify({
            'updated': False,
            'error': str(err)
        }), 500

@app.route('/user', methods=['GET'])
def read() -> Response:
    query_param = request.args.get('id', '')
    
    try: 
      
        user = User.query.get(query_param)
        
        if not user:
            return jsonify({
                'read': False,
                'error': 'User not found'
            }), 404

        return jsonify({
            'read': True,
            'user': user.to_json()
        }), 200
    except Exception as err:
        return jsonify({
            'read': False,
            'error': str(err)
        }), 500

@app.route('/user', methods=['DELETE'])
def delete() -> Response:
    query_param = request.args.get('id', '')
    try: 
        user_deleted = User.query.get(query_param)
        
        if not user_deleted:
            return jsonify({'error': 'No user found to delete'}), 404    
        
        db.session.delete(user_deleted)
        db.session.commit()
        
        return jsonify({
            'deleted': True,
            'user': user_deleted.to_json()
        }), 200
    except Exception as err:
        return jsonify({
            'deleted': False,
            'error': str(err)
        }), 500

if __name__ == '__main__':
    import sys
    if 'pytest' not in sys.modules:
        with app.app_context():
            db.create_all()
        app.run(debug=True)