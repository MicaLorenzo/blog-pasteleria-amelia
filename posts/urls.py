from django.urls import path

from . import views

urlpatterns = [
    path("", views.listado_posts, name="listado_posts"),
    path("buscar/", views.buscar_posts, name="buscar_posts"),
    path("nuevo/", views.crear_post, name="crear_post"),
    path("<slug:slug>/", views.detalle_post, name="detalle_post"),
    path("<slug:slug>/editar/", views.editar_post, name="editar_post"),
    path("<slug:slug>/eliminar/", views.eliminar_post, name="eliminar_post"),
]
