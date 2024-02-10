from config.init_db import db


class Subject(db.Model):
    __tablename__ ='subjects'
    subject_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    professor = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    active = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Subject('{self.name}', '{self.professor}', '{self.semester}', '{self.active}')"
