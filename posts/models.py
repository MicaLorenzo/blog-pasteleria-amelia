from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    titulo = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to="posts/", null=True, blank=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo)
            slug = base_slug
            contador = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                contador += 1
                slug = f"{base_slug}-{contador}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detalle_post", kwargs={"slug": self.slug})
