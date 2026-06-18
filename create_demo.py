# create_demo.py
# Crea usuarios demo y algunas notas para pruebas en NoteSpace
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Note

def create_demo():
    with app.app_context():
        db.create_all()
        users = [
            {'name': 'María López', 'email': 'maria@example.com', 'pw': 'pass123'},
            {'name': 'Carlos Méndez', 'email': 'carlos@example.com', 'pw': 'pass123'},
            {'name': 'Ana Pérez', 'email': 'ana@example.com', 'pw': 'pass123'},
            {'name': 'Luis Rodríguez', 'email': 'luis@example.com', 'pw': 'pass123'},
            {'name': 'Sofía García', 'email': 'sofia@example.com', 'pw': 'pass123'},
        ]

        for u in users:
            if not User.query.filter_by(email=u['email']).first():
                user = User(name=u['name'], email=u['email'], password=generate_password_hash(u['pw']))
                db.session.add(user)
                db.session.commit()
                # crear 2 notas demo por usuario
                n1 = Note(title=f"Nota 1 de {u['name']}", content="Contenido de ejemplo A.", tags="demo,ejemplo", owner=user)
                n2 = Note(title=f"Nota 2 de {u['name']}", content="Contenido de ejemplo B.", tags="tarea,importante", owner=user)
                n3 = Note(title=f"Nota 3 de {u['name']}", content="Contenido de ejemplo C.", tags="demo,ejemplo", owner=user)
                n4 = Note(title=f"Nota 4 de {u['name']}", content="Contenido de ejemplo D.", tags="tarea,importante", owner=user)
                n5 = Note(title=f"Nota 5 de {u['name']}", content="Contenido de ejemplo E.", tags="demo,ejemplo", owner=user)
                n6 = Note(title=f"Nota 6 de {u['name']}", content="Contenido de ejemplo F.", tags="tarea,importante", owner=user)
                n7 = Note(title=f"Nota 7 de {u['name']}", content="Contenido de ejemplo G.", tags="demo,ejemplo", owner=user)
                n8 = Note(title=f"Nota 8 de {u['name']}", content="Contenido de ejemplo H.", tags="tarea,importante", owner=user)
                n9 = Note(title=f"Nota 9 de {u['name']}", content="Contenido de ejemplo I.", tags="demo,ejemplo", owner=user)
                n10 = Note(title=f"Nota 10 de {u['name']}", content="Contenido de ejemplo J.", tags="tarea,importante", owner=user)
                db.session.add_all([n1, n2, n3, n4, n5, n6, n7, n8, n9, n10])
                db.session.commit()
        print("Usuarios demo creados. Contraseña para todos: pass123")

if __name__ == "__main__":
    create_demo()
