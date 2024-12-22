from configs import db
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

db = SQLAlchemy()

class SongInfo(db.Model):
    __tablename__ = 'songrequest'
    id_song = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    song = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)
    def to_dict(self):
        return {
            'id_song': self.id_song,
            'song': self.song,
            'user': self.user,
        }

class SongForm(FlaskForm):
    song = StringField("song")
    user = StringField("user")
    submit = SubmitField("Agregar")