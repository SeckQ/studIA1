from flask import Blueprint, request, jsonify
from .topic_model import db, Topic

topics_bp = Blueprint('topics', __name__)


@topics_bp.route('/topics', methods=['POST'])
def create_topic():
    data = request.get_json()
    new_topic = Topic(topic_name=data['topic_name'],
                      user_id=data['user_id'],
                      subject_id=data['subject_id'])
    db.session.add(new_topic)
    db.session.commit()
    return jsonify({'message': 'Topic created successfully'}), 201


@topics_bp.route('/topics/<int:user_id>', methods=['GET'])
def get_topics(user_id):
    topics = Topic.query.filter_by(user_id=user_id).all()
    topic_list = []
    for topic in topics:
        topic_list.append({'topic_id': topic.topic_id, 'topic_name': topic.topic_name})
    return jsonify({'topics': topic_list})


@topics_bp.route('/topics/<int:topic_id>', methods=['PUT'])
def update_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    data = request.get_json()
    topic.topic_name = data['topic_name']
    db.session.commit()
    return jsonify({'message': 'Topic updated successfully'})


@topics_bp.route('/topics/<int:topic_id>', methods=['DELETE'])
def delete_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    db.session.delete(topic)
    db.session.commit()
    return jsonify({'message': 'Topic deleted successfully'})