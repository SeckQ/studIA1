from flask import Blueprint, request, jsonify
from .subject_model import db, Subject

subjects_bp = Blueprint('subjects', __name__)

@subjects_bp.route('/subjects', methods=['POST'])
def create_subject():
    data = request.get_json()
    new_subject = Subject(name=data['name'],
                          professor=data['professor'],
                          semester=data['semester'],
                          active=data['active'],
                          user_id=data['user_id'])
    db.session.add(new_subject)
    db.session.commit()
    return jsonify({'message': 'Subject created successfully'}), 201


@subjects_bp.route('/subjects/<int:user_id>', methods=['GET'])
def get_subjects(user_id):
    subjects = Subject.query.filter_by(user_id=user_id).all()
    subject_list = []
    for subject in subjects:
        subject_list.append({'subject_id': subject.subject_id, 'name': subject.name, 'professor': subject.professor, 'semester': subject.semester, 'active': subject.active})
    return jsonify({'subjects': subject_list})


@subjects_bp.route('/subjects/<int:subject_id>', methods=['PUT'])
def update_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json()
    subject.type_name = data['name']
    subject.professor = data['professor']
    subject.semester = data['semester']
    subject.active = data['active']
    db.session.commit()
    return jsonify({'message': 'Subject updated successfully'})


@subjects_bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return jsonify({'message': 'Subject deleted successfully'})


@subjects_bp.route('/subjects/<int:user_id>/<int:subject_id>', methods=['GET'])
def get_subject_by_id(user_id, subject_id):
    subject = Subject.query.filter_by(user_id=user_id, subject_id=subject_id).first()
    if subject:
        subject_data = {
            'subject_id': subject.subject_id,
            'name': subject.name,
            'professor': subject.professor,
            'semester': subject.semester,
            'active': subject.active
        }
        return jsonify({'subject': subject_data}), 200
    else:
        return jsonify({'message': 'Subject not found'}), 404