from flask import Flask
from config.config import Config
from users.user_routes import users_bp
from subjects.subject_routes import subjects_bp
from note_types.note_type_routes import note_types_bp
from topics.topic_routes import topics_bp
from notes.note_routes import notes_bp
from ai.questions import ai_bp
from config.init_db import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(users_bp)
app.register_blueprint(subjects_bp)
app.register_blueprint(note_types_bp)
app.register_blueprint(topics_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(ai_bp)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
