from flask import Blueprint, request, jsonify
from .user_model import db, User

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({'id': user.user_id,
                          'first_name': user.first_name,
                          'last_name': user.last_name,
                          'mail': user.mail})
    return jsonify({'users': user_list})


@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(first_name=data['first_name'],
                    last_name=data['last_name'],
                    mail=data['mail'],
                    password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.user_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'mail': user.mail})

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['mail']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validamos las credenciales del usuario de prueba
    if username == 'admin' and password == 'admin':
        return jsonify({'authenticated': True})
    else:
        return jsonify({'authenticated': False})