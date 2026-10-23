import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Post

MEDIA_DE_PRUEBA = tempfile.mkdtemp()


def imagen_de_prueba():
    """Genera una imagen PNG chiquita en memoria para probar la carga."""
    archivo = BytesIO()
    Image.new("RGB", (10, 10), "pink").save(archivo, "PNG")
    return SimpleUploadedFile("torta.png", archivo.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=MEDIA_DE_PRUEBA)
class PostTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_DE_PRUEBA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.amelia = User.objects.create_user("amelia", password="clave-de-prueba-123")
        self.otra = User.objects.create_user("otra", password="clave-de-prueba-123")
        self.post = Post.objects.create(
            titulo="Chocotorta clásica",
            contenido="Galletitas de chocolate, dulce de leche y queso crema.",
            autor=self.amelia,
        )

    # --- Visitante anónimo ---

    def test_listado_y_detalle_son_publicos(self):
        self.assertContains(self.client.get(reverse("listado_posts")), "Chocotorta clásica")
        respuesta = self.client.get(self.post.get_absolute_url())
        self.assertContains(respuesta, "Esta publicación no tiene imagen")

    def test_rutas_protegidas_redirigen_al_login(self):
        rutas = [
            reverse("crear_post"),
            reverse("editar_post", args=[self.post.slug]),
            reverse("eliminar_post", args=[self.post.slug]),
            reverse("perfil"),
            reverse("editar_perfil"),
        ]
        for ruta in rutas:
            respuesta = self.client.get(ruta)
            self.assertRedirects(respuesta, f"{reverse('login')}?next={ruta}")

    def test_anonimo_no_puede_crear_por_post(self):
        self.client.post(reverse("crear_post"), {"titulo": "Torta trucha", "contenido": "x"})
        self.assertFalse(Post.objects.filter(titulo="Torta trucha").exists())

    # --- Usuario autenticado ---

    def test_crear_post_con_imagen(self):
        self.client.login(username="amelia", password="clave-de-prueba-123")
        respuesta = self.client.post(
            reverse("crear_post"),
            {
                "titulo": "Lemon pie",
                "contenido": "Masa sablée, crema de limón y merengue.",
                "imagen": imagen_de_prueba(),
            },
        )
        post = Post.objects.get(titulo="Lemon pie")
        self.assertRedirects(respuesta, post.get_absolute_url())
        self.assertTrue(post.imagen)
        self.assertContains(self.client.get(post.get_absolute_url()), post.imagen.url)

    def test_editar_y_eliminar_post_propio(self):
        self.client.login(username="amelia", password="clave-de-prueba-123")
        self.client.post(
            reverse("editar_post", args=[self.post.slug]),
            {"titulo": "Chocotorta mejorada", "contenido": "Con más dulce de leche."},
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.titulo, "Chocotorta mejorada")

        self.client.post(reverse("eliminar_post", args=[self.post.slug]))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_no_se_puede_editar_post_ajeno(self):
        self.client.login(username="otra", password="clave-de-prueba-123")
        respuesta = self.client.get(reverse("editar_post", args=[self.post.slug]))
        self.assertEqual(respuesta.status_code, 403)

    # --- Búsqueda ---

    def test_busqueda_con_y_sin_resultados(self):
        url = reverse("buscar_posts")
        self.assertContains(self.client.get(url, {"q": "dulce de leche"}), "Chocotorta clásica")
        self.assertContains(self.client.get(url, {"q": "macarons"}), "No se encontraron")