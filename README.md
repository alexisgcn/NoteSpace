# 📝 NoteSpace

Aplicación web de gestión de notas personales desarrollada como proyecto universitario para la materia de **Interacción Hombre-Máquina**.

---

## ✨ Funcionalidades

- **Autenticación de usuarios** — Registro, inicio de sesión y cierre de sesión seguro
- **CRUD de notas** — Crear, leer, editar y eliminar notas personales
- **Etiquetas** — Organiza tus notas con etiquetas personalizadas
- **Búsqueda y filtrado** — Filtra notas por título, contenido o etiqueta
- **Ordenamiento** — Ordena por más reciente, más antiguo o título
- **Papelera** — Las notas eliminadas van a la papelera y se pueden restaurar o eliminar permanentemente
- **Compartir notas** — Genera un enlace público para compartir una nota sin necesidad de iniciar sesión
- **Dashboard** — Vista resumen con conteo de notas y acceso rápido

---

## 🛠 Tecnologías utilizadas

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3 + Flask 3.1 |
| Base de datos | SQLite + Flask-SQLAlchemy |
| Autenticación | Flask-Login + Werkzeug |
| Formularios | Flask-WTF + WTForms |
| Frontend | HTML5, CSS3, JavaScript |
| Templating | Jinja2 |

---

## 🚀 Instalación y uso

### Requisitos previos

- Python 3.10 o superior
- pip

### Pasos

```bash
# 1. Clona el repositorio
git clone https://github.com/alexisgcn/NoteSpace.git
cd NoteSpace

# 2. Crea y activa el entorno virtual
python -m venv venv

# Windows (CMD)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Corre la aplicación
python app.py
```

Luego abre tu navegador en: **http://127.0.0.1:5000**

---

## 📁 Estructura del proyecto

```
NoteSpace/
├── app.py                  # Aplicación principal y rutas
├── models.py               # Modelos de base de datos (User, Note)
├── forms.py                # Formularios (Registro, Login, Nota)
├── requirements.txt        # Dependencias del proyecto
├── instance/
│   └── app.db              # Base de datos SQLite (generada automáticamente)
├── static/
│   ├── css/styles.css      # Estilos de la aplicación
│   ├── js/script.js        # Lógica del frontend
│   └── img/logo.svg        # Logo
└── templates/
    ├── base.html           # Plantilla base
    ├── index.html          # Página de inicio
    ├── dashboard.html      # Panel principal
    ├── notes_list.html     # Lista de notas
    ├── note_detail.html    # Detalle de nota
    ├── note_form.html      # Formulario crear/editar
    ├── note_shared_public.html  # Vista pública compartida
    ├── trash_list.html     # Papelera
    ├── login.html          # Inicio de sesión
    └── register.html       # Registro
```

---

## 👥 Autores

Alexis Carmona

Proyecto desarrollado para la asignatura de **Interacción Hombre-Máquina** — Técnico Superior en Desarrollo de Software, Instituto Técnico Superior Comunitario (ITSC)

---

## 📄 Licencia

Este proyecto es de uso académico.