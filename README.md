# Blog Web — Proyecto Final

Blog web desarrollado con Django, con publicaciones (posts) con imagen, sistema de usuarios con registro/login/logout, perfil de usuario con avatar, rutas protegidas y buscador de posts.

## Tecnologías utilizadas

- Python 3
- Django 5.2
- Pillow (manejo de imágenes)
- SQLite (base de datos de desarrollo)
- HTML / CSS

## Funcionalidades principales

- CRUD completo de posts (listar, ver detalle, crear, editar, eliminar) desde la interfaz web.
- Carga y visualización de imagen por post; el template no se rompe si el post no tiene imagen.
- Registro, login y logout de usuarios.
- Perfil de usuario editable, con avatar opcional.
- El sistema distingue entre usuario anónimo y autenticado (la barra de navegación cambia según el estado de sesión).
- Rutas protegidas: crear, editar y eliminar posts, y editar el perfil, requieren sesión iniciada (`@login_required` en las vistas, no solo ocultar botones).
- Solo el autor de un post puede editarlo o eliminarlo.
- Buscador de posts por título o contenido.

## Instalación y ejecución local

1. Cloná el repositorio y entrá a la carpeta del proyecto.

2. Creá y activá un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate      # En Windows: venv\Scripts\activate
   ```

3. Instalá las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Copiá `.env.example` como `.env` (si tu configuración usa variables de entorno) y completá los valores.

5. Aplicá las migraciones:
   ```bash
   python manage.py migrate
   ```

6. (Opcional) Creá un superusuario para entrar al panel de administración:
   ```bash
   python manage.py createsuperuser
   ```

7. Iniciá el servidor:
   ```bash
   python manage.py runserver
   ```

8. Abrí `http://127.0.0.1:8000/` en el navegador.

## Autor

Proyecto desarrollado como entrega final del Curso Data Analytics — CoderHouse.
