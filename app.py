# app.py
# Aplicación principal para "NoteSpace" (Flask + SQLite + Flask-Login)

from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Importar modelos y formularios
from models import db, User, Note
from forms import RegisterForm, LoginForm, NoteForm

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='templates', static_folder='static')

# Cambia esta clave en producción
app.config['SECRET_KEY'] = 'CAMBIA-ESTA-CLAVE-POR-UNA-SEGURA'

# Base de datos dentro de /instance/app.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar base de datos
db.init_app(app)

# Crear carpeta instance si no existe
os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)

# Crear la DB automáticamente (compatible Flask 3.x)
with app.app_context():
    db.create_all()

# ------------------- CONFIGURACIÓN LOGIN -------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None


# ------------------- RUTAS PÚBLICAS -------------------

@app.route('/')
def index():
    return render_template('index.html')


# ------------------- REGISTRO -------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        existing = User.query.filter_by(email=email).first()

        if existing:
            flash('El correo ya está registrado.', 'warning')
            return redirect(url_for('register'))

        hashed = generate_password_hash(form.password.data)

        user = User(
            name=form.name.data.strip(),
            email=email,
            password=hashed
        )
        db.session.add(user)
        db.session.commit()

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# ------------------- LOGIN -------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Sesión iniciada.', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))

        flash('Correo o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)


# ------------------- LOGOUT -------------------

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('index'))


# ------------------- DASHBOARD -------------------

@app.route('/dashboard')
@login_required
def dashboard():
    count = Note.query.filter_by(user_id=current_user.id, is_deleted=False).count()
    recent = Note.query.filter_by(user_id=current_user.id, is_deleted=False)\
                       .order_by(Note.updated_at.desc()).limit(4).all()

    return render_template('dashboard.html', count=count, recent=recent)


# ------------------- LISTA DE NOTAS -------------------

@app.route('/notes')
@login_required
def notes_list():
    q = request.args.get('q', '').strip()
    tag = request.args.get('tag', '').strip()

    notes_query = Note.query.filter_by(user_id=current_user.id, is_deleted=False)

    if q:
        notes_query = notes_query.filter(
            Note.title.contains(q) |
            Note.content.contains(q) |
            Note.tags.contains(q)
        )

    if tag:
        notes_query = notes_query.filter(Note.tags.contains(tag))

    order = request.args.get('order', '').strip().lower()
    if order == 'new':
        notes_query = notes_query.order_by(Note.updated_at.desc())
    elif order == 'old':
        notes_query = notes_query.order_by(Note.updated_at.asc())
    elif order == 'title':
        notes_query = notes_query.order_by(Note.title.asc())
    else:
        # predeterminado: updated desc (recientes primero)
        notes_query = notes_query.order_by(Note.updated_at.desc())

    notes = notes_query.all()
    #notes = notes_query.order_by(Note.updated_at.desc()).all()

    return render_template('notes_list.html', notes=notes, q=q, tag=tag)


# ------------------- CREAR NOTA -------------------

@app.route('/notes/new', methods=['GET', 'POST'])
@login_required
def notes_new():
    form = NoteForm()

    if form.validate_on_submit():
        tags_raw = form.tags.data or ''
        tags = ','.join([t.strip() for t in tags_raw.split(',') if t.strip()])

        n = Note(
            title=form.title.data.strip(),
            content=form.content.data.strip() if form.content.data else None,
            tags=tags,
            owner=current_user
        )

        db.session.add(n)
        db.session.commit()

        flash('Nota creada.', 'success')
        return redirect(url_for('notes_list'))

    return render_template('note_form.html', form=form, action='Crear')


# ------------------- DETALLE -------------------

@app.route('/notes/<int:note_id>')
@login_required
def notes_detail(note_id):
    n = Note.query.get_or_404(note_id)

    if n.user_id != current_user.id:
        abort(403)

    return render_template('note_detail.html', note=n)


# ------------------- EDITAR NOTA -------------------

@app.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def notes_edit(note_id):
    n = Note.query.get_or_404(note_id)

    if n.user_id != current_user.id:
        abort(403)

    form = NoteForm(obj=n)

    if form.validate_on_submit():
        n.title = form.title.data.strip()
        n.content = form.content.data.strip() if form.content.data else None

        tags_raw = form.tags.data or ''
        n.tags = ','.join([t.strip() for t in tags_raw.split(',') if t.strip()])

        n.updated_at = datetime.utcnow()

        db.session.commit()

        flash('Nota actualizada.', 'success')
        return redirect(url_for('notes_detail', note_id=n.id))

    form.tags.data = n.tags
    return render_template('note_form.html', form=form, action='Editar', note=n)



# ------------------- COMPARTIR NOTA (ENLACE PÚBLICO) -------------------

@app.route('/notes/<int:note_id>/share', methods=['POST'])
@login_required
def notes_toggle_share(note_id):
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:
        abort(403)

    action = request.form.get('action')

    if action == 'enable':
        note.ensure_public_token()
        note.is_public = True
        flash('Enlace público activado para esta nota.', 'success')
    elif action == 'disable':
        note.is_public = False
        flash('Enlace público desactivado.', 'info')

    note.updated_at = datetime.utcnow()
    db.session.commit()

    return redirect(url_for('notes_detail', note_id=note.id))


@app.route('/s/<token>')
def shared_note_view(token):
    note = Note.query.filter_by(public_token=token, is_public=True).first_or_404()
    # Vista de solo lectura, sin necesidad de login
    return render_template('note_shared_public.html', note=note)


# ------------------- PAPELERA -------------------

@app.route('/notes/<int:note_id>/delete', methods=['POST'])
@login_required
def notes_delete(note_id):
    n = Note.query.get_or_404(note_id)

    if n.user_id != current_user.id:
        abort(403)

    n.is_deleted = True
    db.session.commit()

    flash('Nota movida a la papelera.', 'info')
    return redirect(url_for('notes_list'))


@app.route('/trash')
@login_required
def trash_list():
    notes = Note.query.filter_by(user_id=current_user.id, is_deleted=True)\
                      .order_by(Note.updated_at.desc()).all()
    return render_template('trash_list.html', notes=notes)


@app.route('/trash/<int:note_id>/restore', methods=['POST'])
@login_required
def trash_restore(note_id):
    n = Note.query.get_or_404(note_id)

    if n.user_id != current_user.id:
        abort(403)

    n.is_deleted = False
    db.session.commit()

    flash('Nota restaurada.', 'success')
    return redirect(url_for('trash_list'))


@app.route('/trash/<int:note_id>/delete_permanent', methods=['POST'])
@login_required
def trash_delete_permanent(note_id):
    n = Note.query.get_or_404(note_id)

    if n.user_id != current_user.id:
        abort(403)

    db.session.delete(n)
    db.session.commit()

    flash('Nota eliminada permanentemente.', 'danger')
    return redirect(url_for('trash_list'))


# ------------------- CONTEXTO GLOBAL (TAGS) -------------------

@app.context_processor
def inject_tags_to_sidebar():
    if current_user.is_authenticated:
        notes = Note.query.filter_by(user_id=current_user.id, is_deleted=False).all()

        tags_set = set()
        for n in notes:
            if n.tags:
                for t in n.tags.split(','):
                    t = t.strip()
                    if t:
                        tags_set.add(t)

        tags = sorted(tags_set)
    else:
        tags = []

    q = request.args.get('q', '')

    return dict(user_tags=tags, q=q)


# ------------------- EJECUCIÓN -------------------

if __name__ == '__main__':
    app.run(debug=True)
# Nota