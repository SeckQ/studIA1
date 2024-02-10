from config.init_db import db


class NoteType(db.Model):
    __tablename__ = 'note_types'
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    def __repr__(self):
        return f"Type('{self.type_name}', '{self.user_id}')"
