# models.py
# Modelos de la aplicación NoteSpace

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import secrets

db = SQLAlchemy()

# ---------------- USUARIO ----------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notes = db.relationship('Note', backref='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

# ---------------- NOTAS ----------------
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=True)

    tags = db.Column(db.String(200), nullable=True)  # ej: "trabajo,personal"

    is_deleted = db.Column(db.Boolean, default=False)

    public_token = db.Column(db.String(64), unique=True, index=True)
    is_public = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con usuario
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def ensure_public_token(self):
        """Genera un token público si la nota aún no lo tiene."""
        if not self.public_token:
            self.public_token = secrets.token_urlsafe(16)

    def __repr__(self):
        return f"<Note {self.title}>"

