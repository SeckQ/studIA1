from config.init_db import db


class Note(db.Model):
    __tablename__ = 'notes'
    note_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'), nullable=False)
    note_type_id = db.Column(db.Integer, db.ForeignKey('note_types.type_id'), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    last_modification_date = db.Column(db.DateTime, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)
    islearning = db.Column(db.Integer, nullable=False)
    repetition_interval = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return f"Note('{self.title}')"

