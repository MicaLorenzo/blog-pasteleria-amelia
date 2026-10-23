# 🎂 Pastelería Amelia — Blog web con Django

Blog de la Pastelería Amelia, donde se publican recetas, las tortas de la semana y novedades del local. Cualquier visitante puede leer y buscar publicaciones; los usuarios registrados pueden crear las suyas con foto, editarlas o eliminarlas.

Proyecto final de Python.

## Tecnologías utilizadas

- Python 3
- Django 5.2
- Pillow (manejo de imágenes)
- python-decouple (variables de entorno)
- SQLite (base de datos de desarrollo)
- HTML y CSS

## Funcionalidades principales

- **Publicaciones (CRUD completo desde la web):** listar, ver detalle, crear, editar y eliminar.
- **Imágenes:** cada publicación puede tener una foto. Si no tiene, se muestra un recuadro en su lugar y la página no se rompe.
- **Usuarios:** registro, inicio y cierre de sesión.
- **Perfil:** página de perfil con bio y foto de perfil editables.
- **Anónimo vs. autenticado:** la barra de navegación cambia según haya sesión iniciada o no.
- **Rutas protegidas:** crear, editar y eliminar publicaciones, y ver o editar el perfil, requieren sesión iniciada. La protección está en las vistas con `@login_required`: si un visitante entra por URL, lo redirige al login.
- **Permisos:** solo quien escribió una publicación puede editarla o eliminarla.
- **Búsqueda:** busca por título o contenido y avisa cuando no hay resultados.
- **Pruebas automáticas** de las funcionalidades principales.

## Estructura del proyecto

```
blog_config/   Configuración general (settings.py, urls.py)
posts/         App de publicaciones (modelo, vistas, formularios, plantillas y pruebas)
usuarios/      App de usuarios (registro, login, perfil y pruebas)
templates/     Plantilla base compartida (base.html)
static/        Archivos estáticos (css/blog.css)
media/         Imágenes subidas (se crea sola; no está en el repositorio)
```

## Instalación y ejecución local

1. Cloná el repositorio y entrá a la carpeta:
```bash
   git clone https://github.com/MicaLorenzo/blog-pasteleria-amelia.git
   cd blog-pasteleria-amelia
```

2. Creá y activá un entorno virtual:
```bash
   python -m venv venv

   # Windows (Git Bash)
   source venv/Scripts/activate
   # Windows (CMD o PowerShell)
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
```

3. Instalá las dependencias:
```bash
   pip install -r requirements.txt
```

4. Creá el archivo `.env` a partir del ejemplo:
```bash
   cp .env.example .env
```
   Abrí `.env` y reemplazá `SECRET_KEY` por una clave propia. Podés generar una con:
```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
   Dejá `DEBUG=True` para desarrollo (así se ven las imágenes subidas).

5. Aplicá las migraciones (crea la base de datos `db.sqlite3`):
```bash
   python manage.py migrate
```

6. (Opcional) Creá un superusuario para entrar al panel de administración en `/admin/`:
```bash
   python manage.py createsuperuser
```

7. Iniciá el servidor:
```bash
   python manage.py runserver
```

8. Abrí `http://127.0.0.1:8000/` en el navegador.

## Cómo probarlo desde cero

El repositorio no incluye `db.sqlite3` ni la carpeta `media/`, así que el blog arranca vacío. Para probarlo:

1. Entrá a **Registrarme** y creá una cuenta.
2. Iniciá sesión y usá **Nueva publicación** para crear una publicación con foto y otra sin foto.
3. Editá y eliminá una publicación desde su página de detalle.
4. Usá **Buscar** con una palabra que exista y con otra que no.
5. Cerrá sesión y entrá a `http://127.0.0.1:8000/nuevo/`: tiene que redirigir al login.

También se pueden correr las pruebas automáticas:

```bash
python manage.py test
```

## Rutas principales

| Ruta | Qué hace | ¿Requiere sesión? |
|---|---|---|
| `/` | Listado de publicaciones | No |
| `/<slug>/` | Detalle de una publicación | No |
| `/buscar/` | Búsqueda | No |
| `/nuevo/` | Crear publicación | Sí |
| `/<slug>/editar/` | Editar publicación | Sí (y ser autor/a) |
| `/<slug>/eliminar/` | Eliminar publicación | Sí (y ser autor/a) |
| `/usuarios/registro/` | Registro | No |
| `/usuarios/login/` | Iniciar sesión | No |
| `/usuarios/perfil/` | Ver perfil | Sí |
| `/usuarios/perfil/editar/` | Editar perfil | Sí |
| `/admin/` | Panel de administración | Superusuario |

## Autora

**Micaela Lorenzo** — [GitHub: MicaLorenzo](https://github.com/MicaLorenzo)

Proyecto final de Python.