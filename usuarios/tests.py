from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UsuarioTests(TestCase):
    def test_registro_login_y_logout(self):
        respuesta = self.client.post(
            reverse("registro"),
            {
                "username": "cliente",
                "email": "cliente@ejemplo.com",
                "password1": "UnaClaveLarga-2026",
                "password2": "UnaClaveLarga-2026",
            },
        )
        self.assertRedirects(respuesta, reverse("login"))
        self.assertTrue(User.objects.filter(username="cliente").exists())

        respuesta = self.client.post(
            reverse("login"), {"username": "cliente", "password": "UnaClaveLarga-2026"}
        )
        self.assertRedirects(respuesta, reverse("listado_posts"))
        self.assertContains(self.client.get(reverse("perfil")), "cliente")

        self.client.post(reverse("logout"))
        respuesta = self.client.get(reverse("listado_posts"))
        self.assertContains(respuesta, "Iniciar sesión")

    def test_email_repetido_no_se_puede_registrar(self):
        User.objects.create_user("amelia", email="amelia@ejemplo.com", password="x")
        respuesta = self.client.post(
            reverse("registro"),
            {
                "username": "otra",
                "email": "amelia@ejemplo.com",
                "password1": "UnaClaveLarga-2026",
                "password2": "UnaClaveLarga-2026",
            },
        )
        self.assertContains(respuesta, "Ya existe una cuenta registrada con ese email")