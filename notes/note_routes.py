from flask import Blueprint, request, jsonify
from datetime import datetime
from .note_model import db, Note

notes_bp = Blueprint('notes', __name__)


@notes_bp.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    new_note = Note(
        title=data['title'],
        content=data['content'],
        topic_id=data['topic_id'],
        note_type_id=data['note_type_id'],
        creation_date=datetime.now(),
        last_modification_date=datetime.now(),
        subject_id=data['subject_id'],
        islearning=data['islearning'],
        repetition_interval=data['repetition_interval'],
        user_id=data['user_id']
    )
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'Note created successfully'}), 201


@notes_bp.route('/notes/<int:user_id>', methods=['GET'])
def get_notes(user_id):
    notes = Note.query.filter_by(user_id=user_id).all()
    note_list = []
    for note in notes:
        note_list.append({
            'note_id': note.note_id,
            'title': note.title,
            'content': note.content,
            'topic_id': note.topic_id,
            'note_type_id': note.note_type_id,
            'creation_date': note.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
            'last_modification_date': note.last_modification_date.strftime('%Y-%m-%d %H:%M:%S'),
            'subject_id': note.subject_id,
            'islearning': note.islearning,
            'repetition_interval': note.repetition_interval
        })
    return jsonify({'notes': note_list})


@notes_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.get_json()
    note.title = data['title']
    note.content = data['content']
    note.topic_id = data['topic_id']
    note.note_type_id = data['note_type_id']
    note.last_modification_date = datetime.now()
    note.subject_id = data['subject_id']
    note.islearning = data['islearning']
    note.repetition_interval = data['repetition_interval']
    db.session.commit()
    return jsonify({'message': 'Note updated successfully'})


@notes_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully'})


@notes_bp.route('/notes/<int:user_id>/<string:materia>', methods=['GET'])
def get_notes_by_subject(user_id, materia):
    # Filtra las notas por el id del usuario y el tema especificado
    notes = Note.query.filter_by(user_id=user_id, subject_id=materia).all()
    note_list = []
    for note in notes:
        note_list.append({
            'note_id': note.note_id,
            'title': note.title,
            'content': note.content,
            'topic_id': note.topic_id,
            'note_type_id': note.note_type_id,
            'creation_date': note.creation_date.strftime('%Y-%m-%d %H:%M:%S'),
            'last_modification_date': note.last_modification_date.strftime('%Y-%m-%d %H:%M:%S'),
            'subject_id': note.subject_id,
            'islearning': note.islearning,
            'repetition_interval': note.repetition_interval
        })
    return jsonify({'notes': note_list})
