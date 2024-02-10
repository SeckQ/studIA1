from flask import Blueprint, request, jsonify
from .note_type_model import db, NoteType

note_types_bp = Blueprint('note_types', __name__)


@note_types_bp.route('/note_types', methods=['POST'])
def create_type():
    data = request.get_json()
    new_type = NoteType(type_name=data['type_name'],
                        user_id=data['user_id'])
    db.session.add(new_type)
    db.session.commit()
    return jsonify({'message': 'Type created successfully'}), 201


@note_types_bp.route('/note_types/<int:user_id>', methods=['GET'])
def get_types(user_id):
    types = NoteType.query.filter_by(user_id=user_id).all()
    type_list = []
    for type in types:
        type_list.append({'type_id': type.type_id, 'type_name': type.type_name})
    return jsonify({'note_types': type_list})


@note_types_bp.route('/note_types/<int:type_id>', methods=['PUT'])
def update_type(type_id):
    type = NoteType.query.get_or_404(type_id)
    data = request.get_json()
    type.type_name = data['type_name']
    db.session.commit()
    return jsonify({'message': 'Type updated successfully'})


@note_types_bp.route('/note_types/<int:type_id>', methods=['DELETE'])
def delete_type(type_id):
    type = NoteType.query.get_or_404(type_id)
    db.session.delete(type)
    db.session.commit()
    return jsonify({'message': 'Type deleted successfully'})